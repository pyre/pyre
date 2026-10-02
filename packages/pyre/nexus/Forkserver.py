# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import pickle
import select
import signal
import socket
import subprocess
import sys
import time
import traceback

# support
import pyre
from ..units.SI import second

# my superclass
from .Fork import Fork


# the command line of this process, as it was launched: the interpreter, its own options, the
# script, and the arguments of the script; the script is made absolute now, before anybody has
# a chance to change the working directory, so the helper runs the same one
def launch():
    """
    Reconstruct the command line that launched this process, with the script made absolute
    """
    # the full command line, interpreter and interpreter options included
    original = list(sys.orig_argv)
    # the part the script sees starts with the script itself
    start = len(original) - len(sys.argv)
    # a script that ran from a file
    if 0 < start < len(original) and os.path.exists(original[start]):
        # gets pinned down
        original[start] = os.path.abspath(original[start])
    # hand off the command line
    return original


# captured once, when the recruiter is imported
command = launch()
# the part of it that names the interpreter, its options, and the script
script = command[: len(command) - len(sys.argv) + 1]


def fingerprint():
    """
    Describe what this process is running, so a helper can prove it runs the same thing
    """
    # the pieces that must agree
    return {
        # the interpreter
        "executable": os.path.realpath(sys.executable),
        # the installation of the framework
        "pyre": os.path.realpath(pyre.__file__),
        # the interpreter options and the script; the arguments that follow are the same by
        # construction, except for the ones that select the helper shell
        "script": script,
    }


def origin(cls):
    """
    Find the file the module that defines {cls} was loaded from
    """
    # get the module
    module = sys.modules.get(cls.__module__)
    # get its file, if it has one
    file = getattr(module, "__file__", None)
    # and resolve it, so two spellings of the same file agree
    return os.path.realpath(file) if file is not None else None


# the helper, as seen from the process that spawned it
class Helper:
    """
    A clean copy of the application that forks crew members on request

    The helper is spawned, not forked, from the command line of the application, so it runs
    the same code under the same configuration, but it never does anything but wait for
    requests; the members it forks are copies of a process that has touched nothing, whatever
    the process that asks for them has touched since it started
    """

    # interface
    def recruit(self, crew, transport, channel, journal):
        """
        Ask for a new crew member built from the class {crew}, talking over the {transport}
        with the descriptors in {channel} and, when there is one, {journal}; hand back its pid
        """
        # the request
        request = {
            # the class of the member, pickled; the helper passes it along without loading it,
            # so the member is the one that imports its module, after the fork, and the helper
            # stays as clean as it started
            "recruit": pickle.dumps(crew),
            # the file its module was loaded from here, which is where the member must load it
            "origin": origin(crew),
            # the kind of channel it talks over
            "transport": transport,
            # how many of the descriptors belong to the crew channel
            "channel": len(channel),
            # and whether there is a journal channel
            "journal": journal is not None,
        }
        # the descriptors travel with the request
        descriptors = list(channel) + (list(journal) if journal is not None else [])
        # send it
        self.send(message=request, descriptors=descriptors)
        # and wait for the answer
        answer = self.expect(key="recruited")
        # hand off the pid of the new member
        return answer["recruited"]

    def instruct(self, control):
        """
        Pass the journal {control} to the helper, so the members it forks from now on start
        with it in place
        """
        # send it in its wire form
        self.send(message={"instruct": control.encode()})
        # all done
        return self

    def exited(self, pid, patience):
        """
        Wait up to {patience} seconds for the helper to report that the member {pid} exited;
        with no {patience}, wait for as long as it takes. Report whether it did
        """
        # set the deadline
        deadline = None if patience is None else time.monotonic() + patience
        # until the report is in
        while pid not in self.exits:
            # figure out how long to wait
            wait = None if deadline is None else max(0.0, deadline - time.monotonic())
            # if time is up
            if wait == 0.0:
                # it has not left yet
                return False
            # otherwise, collect whatever the helper says in the meantime
            if not self.receive(timeout=wait):
                # a helper that is gone reports nothing more; check on the member directly
                return self.gone(pid=pid)
        # the report is in; forget it
        del self.exits[pid]
        # and say so
        return True

    def listen(self, dispatcher):
        """
        Hear the journal entries of the helper on the event loop of {dispatcher}, unless they
        are heard already
        """
        # if somebody is listening
        if self.listening:
            # there is nothing to do
            return self
        # listen
        dispatcher.whenReadReady(channel=self, call=self.overhear)
        # and remember it
        self.listening = True
        # all done
        return self

    def alive(self):
        """
        Check whether the helper is still running
        """
        # ask the process
        return self.process.poll() is None

    def stop(self):
        """
        Send the helper home
        """
        # carefully, since it may be gone already
        try:
            # closing my end of the control channel is how the helper is told to leave
            self.control.close()
        # if the channel is gone
        except OSError:
            # there is nothing to close
            pass
        # give it a moment
        try:
            # to leave on its own
            self.process.wait(timeout=2)
        # if it will not
        except subprocess.TimeoutExpired:
            # make it
            self.process.kill()
            # and collect it
            self.process.wait()
        # all done
        return self

    # metamethods
    def __init__(self, shell, dispatcher=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the control channel: datagrams, so each request keeps its own descriptors
        mine, theirs = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM)
        # the channel that carries the journal entries of the helper itself
        journal, theirJournal = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        # the command line of the helper: the application's own, in the helper shell
        argv = command + [
            # select the shell
            f"--shell={shell}",
            # tell it where the control channel is
            f"--shell.control={theirs.fileno()}",
            # and where its journal goes
            f"--shell.journal={theirJournal.fileno()}",
        ]
        # spawn it, with the same environment and working directory, handing it its two ends
        self.process = subprocess.Popen(
            argv, pass_fds=(theirs.fileno(), theirJournal.fileno()), close_fds=True
        )
        # its ends are its own now
        theirs.close()
        theirJournal.close()
        # keep mine
        self.control = mine
        self.journal = journal
        # the exit reports that have arrived and nobody asked for yet
        self.exits = {}
        # the answers that have arrived and nobody asked for yet
        self.answers = []
        # the start of a journal record still in transit
        self.tail = b""
        # nobody is listening to the journal yet
        self.listening = False
        # if there is an event loop to hear the journal on
        if dispatcher is not None:
            # listen to it there
            self.listen(dispatcher=dispatcher)
        # the first thing the helper says is what it is running
        hello = self.expect(key="hello")
        # which must be what i am running
        mine = fingerprint()
        # if it is not
        if hello["hello"] != mine:
            # get the journal
            import journal

            # make a channel
            channel = journal.firewall("pyre.nexus.forkserver")
            # complain
            channel.line("the helper does not run what this process runs")
            channel.indent()
            # go through the pieces
            for key, value in mine.items():
                # show the ones that differ
                if hello["hello"].get(key) != value:
                    # side by side
                    channel.line(f"{key}: {value!r} here, {hello['hello'].get(key)!r} there")
            # flush
            channel.log()
        # all done
        return

    # implementation details
    def send(self, message, descriptors=()):
        """
        Send {message} to the helper, along with any open {descriptors}
        """
        # encode the message
        payload = pickle.dumps(message)
        # if there are descriptors
        if descriptors:
            # they travel as ancillary data
            socket.send_fds(self.control, [payload], list(descriptors))
        # otherwise
        else:
            # the message goes alone
            self.control.send(payload)
        # all done
        return

    def expect(self, key, patience=30.0):
        """
        Wait for the answer that carries {key}, collecting exit reports along the way
        """
        # set the deadline
        deadline = time.monotonic() + patience
        # until the answer is in
        while True:
            # go through the answers that are in
            for index, answer in enumerate(self.answers):
                # if this is the one
                if key in answer:
                    # take it off the pile
                    del self.answers[index]
                    # and hand it off
                    return answer
            # figure out how long to wait
            wait = deadline - time.monotonic()
            # if the helper is gone or has taken too long
            if wait <= 0 or not self.receive(timeout=wait):
                # get the journal
                import journal

                # make a channel
                channel = journal.firewall("pyre.nexus.forkserver")
                # complain
                channel.line(f"the helper did not answer with '{key}'")
                channel.line(f"helper: pid {self.process.pid}, exit status {self.process.poll()}")
                # flush
                channel.log()
                # and bail, in case firewalls are not fatal
                return None

    def receive(self, timeout):
        """
        Collect one message from the helper, waiting up to {timeout} seconds; report whether
        the helper is still there
        """
        # wait for something to read
        ready, _, _ = select.select([self.control], [], [], timeout)
        # if nothing came
        if not ready:
            # the helper is still there, as far as anybody knows
            return self.alive()
        # carefully
        try:
            # read one message
            payload = self.control.recv(64 * 1024)
        # if the channel broke
        except OSError:
            # the helper is gone
            return False
        # an empty message
        if not payload:
            # means the helper is gone
            return False
        # decode it
        message = pickle.loads(payload)
        # an exit report
        if "exited" in message:
            # goes on the pile of exits
            self.exits[message["exited"]] = message["status"]
        # anything else
        else:
            # is an answer
            self.answers.append(message)
        # the helper is still there
        return True

    def gone(self, pid):
        """
        Check whether the process {pid} is gone, without being its parent
        """
        # carefully
        try:
            # probe it
            os.kill(pid, 0)
        # if there is no such process
        except ProcessLookupError:
            # it is gone
            return True
        # otherwise, it is still around
        return False

    def overhear(self, channel, **kwds):
        """
        Replay the journal entries of the helper itself, as they arrive
        """
        # get the journal
        import journal

        # carefully
        try:
            # read what is there
            data = self.journal.recv(64 * 1024)
        # if the channel broke
        except OSError:
            # stop listening
            self.listening = False
            # and let the event loop know
            return False
        # an empty read
        if not data:
            # means the helper is gone; stop listening
            self.listening = False
            # and let the event loop know
            return False
        # add it to what is in transit
        data = self.tail + data
        # split off the complete records
        *records, self.tail = data.split(b"\n")
        # go through them
        for line in records:
            # carefully
            try:
                # decode it
                record = journal.record.decode(line)
            # if it cannot be understood
            except journal.exceptions.RecordError:
                # skip it
                continue
            # and replay it here
            journal.replay(record=record)
        # keep listening
        return True

    # the event loop watches the journal channel through me
    @property
    def inbound(self):
        """
        The descriptor of the journal channel of the helper
        """
        # easy enough
        return self.journal.fileno()


# declaration
class Forkserver(Fork, family="pyre.nexus.recruiters.forkserver"):
    """
    Create worker processes by asking a helper process to fork them

    The helper is a clean copy of the application, spawned from its command line the first time
    it is needed and kept for the life of the process. Crew members are forked by the helper, so
    they inherit the state of the application as it was at startup, and nothing that the team's
    process has done since, e.g. the threads of a library it has used, which do not survive a
    fork and leave a member waiting forever on one that does not exist on its side

    Whatever a member needs that is set after startup has to travel with its tasks, or be sent
    to it: the journal controls a team applies reach the helper too, so the members it forks
    from then on start with them in place
    """

    # user configurable state
    shell = pyre.properties.str(default="forkserver")
    shell.doc = "the shell that turns a copy of the application into the helper"

    # interface
    @classmethod
    def start(cls, shell=None, dispatcher=None):
        """
        Make sure the helper is running, starting it with {shell} if necessary, and listening
        to its journal on {dispatcher}; applications that fork crew members after they have
        touched libraries with threads of their own start it early, before they do
        """
        # get the helper
        helper = Forkserver._helper
        # if it is running
        if helper is not None and helper.alive():
            # and there is an event loop to hear it on
            if dispatcher is not None:
                # make sure its journal is heard
                helper.listen(dispatcher=dispatcher)
            # there is nothing else to do
            return helper
        # otherwise, start one
        helper = Helper(shell=shell or cls.shell, dispatcher=dispatcher)
        # remember it
        Forkserver._helper = helper
        # and hand it off
        return helper

    @classmethod
    def stop(cls):
        """
        Send the helper home, if there is one
        """
        # get the helper
        helper = Forkserver._helper
        # if there is one
        if helper is not None:
            # send it home
            helper.stop()
            # and forget it
            Forkserver._helper = None
        # all done
        return

    # protocol obligations
    @pyre.provides
    def deploy(self, team, **kwds):
        """
        Create a new {team} member by asking the helper to fork it
        """
        # the helper forks members with nothing but what it is sent
        if kwds:
            # get the journal
            import journal

            # make a channel
            channel = journal.firewall("pyre.nexus.forkserver")
            # complain
            channel.line("the helper cannot build a crew member with arguments")
            channel.line(f"arguments: {sorted(kwds)}")
            # flush
            channel.log()
        # get the helper, starting it if necessary
        helper = self.start(shell=self.shell, dispatcher=team.dispatcher)
        # team members communicate with the manager over my transport; the {child} end is
        # destined for the worker, the {parent} end stays with the team
        parent, child = self.channels.open()
        # the worker's journal entries travel back over a channel of their own, when wanted
        parentJournal, childJournal = self.channels.open() if self.journal else (None, None)
        # ask the helper for a new member of the kind the team employs
        pid = helper.recruit(
            crew=team.crew,
            transport=self.transport(channel=child),
            channel=self.descriptors(channel=child),
            journal=self.descriptors(channel=childJournal) if childJournal is not None else None,
        )
        # the worker's ends are the helper's business now; release mine
        child.close()
        # and the worker's end of the journal channel, if there is one
        if childJournal is not None:
            # release it
            childJournal.close()
        # make a member proxy for the team manager and return it
        crew = team.crew(pid=pid, channel=parent, journal=parentJournal, timer=team.timer)
        # adjust its support for asynchrony
        crew.dispatcher = team.dispatcher
        # and its message serializer
        crew.marshaler = team.marshaler
        # spin it up and return it
        return crew.join(team=team)

    @pyre.provides
    def dismiss(self, team, crew, **kwds):
        """
        The {team} manager has dismissed the given {member}

        As with {fork}, the member gets a grace period to leave on its own, and is then told,
        and then made, to go; the difference is that the member is the helper's child, so it is
        the helper that reports its exit
        """
        # get the process id of the member
        pid = crew.pid
        # and the grace period, in seconds
        grace = self.grace / second
        # get the helper
        helper = Forkserver._helper
        # without one, the member is on its own
        if helper is None:
            # so all that can be done is make sure it is gone
            return self.insist(pid=pid)
        # give it a chance to leave on its own
        if helper.exited(pid=pid, patience=grace):
            # which is how this is supposed to go
            return
        # go through the ways to insist, from polite to final
        for reminder in (signal.SIGTERM, signal.SIGKILL):
            # carefully
            try:
                # remind it
                os.kill(pid, reminder)
            # if it is already gone
            except ProcessLookupError:
                # there is nobody to remind
                break
            # and wait again
            if helper.exited(pid=pid, patience=grace):
                # it left
                return
        # all done
        return

    @pyre.provides
    def instruct(self, control):
        """
        Pass the journal {control} to the helper, so the members it forks later inherit it
        """
        # get the helper
        helper = Forkserver._helper
        # if there is one
        if helper is not None:
            # pass the control along
            helper.instruct(control=control)
        # all done
        return

    # the helper side
    def serve(self, control, journal=None):
        """
        Serve recruitment requests arriving on the {control} descriptor until the process that
        started me is gone; my own journal entries go down the {journal} descriptor
        """
        # the interrupt key reaches the whole process group, but i leave when my parent does
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # note who started me
        parent = os.getppid()
        # dress the control channel
        channel = socket.socket(fileno=control)
        # if my journal is to be routed
        courier = self.courier(descriptor=journal) if journal is not None else None
        # say what i am running
        channel.send(pickle.dumps({"hello": fingerprint()}))
        # serve until my parent is gone
        while os.getppid() == parent:
            # report the members that exited
            self.harvest(channel=channel)
            # wait a little for a request
            ready, _, _ = select.select([channel], [], [], 0.1)
            # if there is none
            if not ready:
                # check again
                continue
            # carefully
            try:
                # pick up the request and the descriptors that came with it
                payload, descriptors, _, _ = socket.recv_fds(channel, 64 * 1024, 16)
            # if the channel broke
            except OSError:
                # there is nobody left to serve
                break
            # an empty request
            if not payload:
                # means my parent let go
                break
            # decode it
            request = pickle.loads(payload)
            # a recruitment request
            if "recruit" in request:
                # fork the member; this returns only on my side of the fork
                pid = self.enlist(
                    request=request, descriptors=descriptors, control=channel, courier=courier
                )
                # tell my parent who it is
                channel.send(pickle.dumps({"recruited": pid}))
                # and move on
                continue
            # a journal control
            if "instruct" in request:
                # get the wire form of controls
                from journal import control as Control

                # apply it here, so the members i fork from now on start with it in place
                Control.decode(request["instruct"]).apply()
                # and move on
                continue
        # all done
        return 0

    # implementation details
    def enlist(self, request, descriptors, control, courier):
        """
        Fork a new crew member as described by {request}, talking over {descriptors}
        """
        # fork
        pid = os.fork()
        # on my side
        if pid > 0:
            # the descriptors belong to the member now
            for descriptor in descriptors:
                # so release my copies
                os.close(descriptor)
            # and hand back its pid
            return pid
        # in the member: whatever happens from here on, this process must never return into the
        # loop of the helper
        try:
            # become the member; this does not return
            self.member(request=request, descriptors=descriptors, control=control, courier=courier)
        # if something let an exception through before the member could leave
        finally:
            # get the complaint of the journal, which has already said what it was about
            from journal.exceptions import JournalError

            # get the exception in flight, if there is one
            error = sys.exc_info()[1]
            # if there is one the journal has not reported
            if error is not None and not isinstance(error, JournalError):
                # say what it was, since the interpreter will not get the chance
                traceback.print_exc()
            # and end the process
            os._exit(1)

    def member(self, request, descriptors, control, courier):
        """
        Turn this fresh fork of the helper into the crew member described by {request}
        """
        # the control channel is the helper's business
        control.close()
        # and so is the helper's journal channel
        if courier is not None:
            # release it
            courier.close()
            # if the member does not route its journal
            if not request["journal"]:
                # get the keeper of the journal devices, and the console device
                from journal import chronicler, cout

                # it speaks to the console, as a member forked from the team would
                chronicler.device = cout()
        # split the descriptors
        channelDescriptors = descriptors[: request["channel"]]
        journalDescriptors = descriptors[request["channel"] :]
        # get the transport
        transport = self.transports[request["transport"]]()
        # dress the crew channel
        channel = self.wrap(transport=transport, descriptors=channelDescriptors)
        # and the journal channel, if there is one
        journal = (
            self.wrap(transport=transport, descriptors=journalDescriptors)
            if request["journal"]
            else None
        )
        # route my journal to the team first, so whatever goes wrong from here on is heard there
        courier = self.route(channel=journal) if journal is not None else None
        # get the class of the member; this imports its module, here, after the fork
        crewClass = pickle.loads(request["recruit"])
        # if its module did not come from where it came from in the team's process
        if origin(crewClass) != request["origin"]:
            # get the journal
            import journal as chronicle

            # make a channel
            firewall = chronicle.firewall("pyre.nexus.forkserver")
            # complain
            firewall.line(f"the crew class '{crewClass.__qualname__}' was loaded from")
            firewall.indent()
            firewall.line(f"{origin(crewClass)} in the member, but from")
            firewall.line(f"{request['origin']} in the team's process")
            firewall.outdent()
            # flush; firewalls are fatal
            firewall.log()
        # make a team member
        crew = crewClass(pid=os.getpid(), channel=channel, journal=journal)
        # which keeps the device that ships its journal alive for as long as it lives
        crew.courier = courier
        # ask it to register with the team
        crew.register()
        # assume the worst, so that anything that goes wrong is reported as a failure
        status = 1
        # and keep track of whether the member got to finish
        crashed = True
        # carefully, since an interrupt may have landed before it was set aside
        try:
            # spin up and carry out tasks until there is nothing more to do
            status = crew.run()
            # the member ran its course
            crashed = False
        # if it did
        except KeyboardInterrupt:
            # leave quietly; the team reports the interruption
            status = 1
            # and this is not a crash
            crashed = False
        # a request to exit
        except SystemExit as request:
            # carries the status it asks for
            status = request.code
            # and is not a crash either
            crashed = False
        # whatever happened, this process must terminate, and it must do so here
        finally:
            # so leave; this does not return
            self.leave(crew=crew, status=status, crashed=crashed)

    def harvest(self, channel):
        """
        Collect the members that exited and report them down {channel}
        """
        # as long as there are any
        while True:
            # carefully
            try:
                # ask, without waiting
                pid, status = os.waitpid(-1, os.WNOHANG)
            # with no children at all
            except ChildProcessError:
                # there is nothing to collect
                return
            # with none that exited
            if pid == 0:
                # there is nothing to collect either
                return
            # report the one that did
            channel.send(pickle.dumps({"exited": pid, "status": status}))

    def courier(self, descriptor):
        """
        Send everything this process says to the journal down {descriptor}
        """
        # get the journal
        import journal

        # make the device
        courier = journal.courier(descriptor=descriptor)
        # install it
        journal.chronicler.device = courier
        # and hand it off
        return courier

    def transport(self, channel):
        """
        Name the kind of {channel}, so the helper can dress its descriptors the same way
        """
        # a socket
        if isinstance(channel, socket.socket):
            # is one descriptor
            return "socket"
        # anything else is a pair of pipes
        return "pipe"

    def descriptors(self, channel):
        """
        Collect the descriptors of {channel}
        """
        # a socket
        if isinstance(channel, socket.socket):
            # is one descriptor
            return [channel.fileno()]
        # a pair of pipes is two
        return [channel.inbound, channel.outbound]

    def wrap(self, transport, descriptors):
        """
        Dress {descriptors} as a channel of {transport}
        """
        # a socket
        if len(descriptors) == 1:
            # is one descriptor
            return transport.wrap(descriptor=descriptors[0])
        # a pair of pipes is two
        return transport.wrap(infd=descriptors[0], outfd=descriptors[1])

    # the transports, by the name they travel under
    transports = {
        "pipe": pyre.ipc.pipe(),
        "socket": pyre.ipc.socket(),
    }

    # the helper of this process, shared by every team
    _helper = None


# end of file
