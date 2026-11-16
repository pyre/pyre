# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import subprocess

# support
import pyre

# the channel the liaison talks to the agency over
from ..ipc.SocketPair import SocketPair

# the marker the marshaler raises when its peer goes away
from ..ipc.exceptions import EndOfStream

# the agency, which knows what this process runs
from .StaffingAgency import StaffingAgency

# what the liaison says and hears
from .messages.Message import Message
from .messages.Instruct import Instruct


# declaration
class Liaison(pyre.component, family="pyre.nexus.liaisons.staffing"):
    """
    The staffing agency's representative in the process whose teams it serves

    The liaison spawns the agency from the command line of the application and talks to it over
    two channels, each with a single reader. On the control channel it sends the recruitment
    requests and the journal controls, and reads the answers itself, synchronously; on the report
    channel the agency reports the exits of its members, which the liaison hears on the event
    loops of the teams and turns into events there. There is one per process, reached by name, so
    every recruiter that uses the agency uses the same one
    """

    # user configurable state
    shell = pyre.properties.str(default="forkserver")
    shell.doc = "the shell that turns a copy of the application into the staffing agency"

    # how the messages on the control and report channels are encoded
    marshaler = pyre.ipc.marshaler()
    marshaler.doc = "the serializer of the messages on the control and report channels"

    # interface
    @classmethod
    def instance(cls) -> "Liaison":
        """
        The liaison of this process
        """
        # the framework hands back the instance it already has under this name
        return cls(name="pyre.nexus.liaison")

    def start(self, dispatcher=None) -> "Liaison":
        """
        Make sure the agency is running, and that its journal and its reports are heard on
        {dispatcher}; applications that fork crew members after they have touched libraries with
        threads of their own start it early, before they do
        """
        # if the agency is not running
        if not self.running():
            # spawn it
            self.spawn()
        # if there is an event loop to hear it on
        if dispatcher is not None:
            # listen there
            self.listen(dispatcher=dispatcher)
        # all done
        return self

    def running(self) -> bool:
        """
        Check whether the agency is running
        """
        # it is, if it was spawned and has not exited
        return self.process is not None and self.process.poll() is None

    def recruit(self, request) -> list[int]:
        """
        Send the recruitment {request} and wait for the pids of its members; the answer is a
        local round trip on a channel nobody else reads, so recruitment stays synchronous
        """
        # no answer yet
        self.answer = None
        # send the request
        request.send(channel=self.control, marshaler=self.marshaler)
        # the control channel carries nothing but answers, so the next message is this one's
        self.hear(channel=self.control)
        # get the journal
        import journal

        # if it is not
        if self.answer is None:
            # make a channel
            channel = journal.firewall("pyre.nexus.staffing")
            # complain
            channel.line("the staffing agency did not answer a recruitment request")
            # flush
            channel.log()
            # and bail, in case firewalls are not fatal
            return []
        # say who they are
        journal.debug("pyre.nexus.staffing").log(f"the agency recruited {self.answer.pids}")
        # and hand off the pids
        return self.answer.pids

    def instruct(self, control) -> "Liaison":
        """
        Pass the journal {control} to the agency, so the members it forks from now on start with
        it in place
        """
        # if the agency is running
        if self.running():
            # send it in its wire form
            Instruct(control=control.encode()).send(channel=self.control, marshaler=self.marshaler)
        # all done
        return self

    def subscribe(self, call) -> "Liaison":
        """
        Arrange for {call} to be invoked whenever the agency reports an exit; it stays subscribed
        for as long as it returns a true value, just like an event handler
        """
        # add it to the pile
        self.subscribers.append(call)
        # all done
        return self

    def collect(self, pid: int) -> tuple:
        """
        Check whether the agency has reported the member {pid} gone; report whether it has, and
        the exit status the agency collected
        """
        # if the agency reported it
        if pid in self.exits:
            # it is gone; take the report off the pile
            return True, self.exits.pop(pid)
        # a member whose agency is gone was reparented to {init}, which reaps it; it is gone if
        # its process is
        if not self.running():
            # carefully
            try:
                # probe it
                os.kill(pid, 0)
            # if there is no such process
            except ProcessLookupError:
                # it is gone, with nothing to report
                return True, None
        # otherwise, it is still around
        return False, None

    def stop(self) -> "Liaison":
        """
        Send the agency home
        """
        # if it was never spawned
        if self.process is None:
            # there is nothing to do
            return self
        # letting go of my end of the control channel is how the agency is told to leave
        self.control.close()
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
        # forget it
        self.process = None
        # all done
        return self

    # message handlers
    def greeted(self, greeting):
        """
        The agency described what it runs; it must be what this process runs
        """
        # what this process runs
        mine = StaffingAgency.fingerprint()
        # if the agency runs the same thing
        if greeting.fingerprint == mine:
            # all is well
            return self
        # otherwise, get the journal
        import journal

        # make a channel
        channel = journal.firewall("pyre.nexus.staffing")
        # complain
        channel.line("the staffing agency does not run what this process runs")
        # set the details apart
        channel.indent()
        # go through the pieces
        for key, value in mine.items():
            # show the ones that differ
            if greeting.fingerprint.get(key) != value:
                # side by side
                channel.line(f"{key}: {value!r} here, {greeting.fingerprint.get(key)!r} there")
        # flush
        channel.log()
        # and bail, in case firewalls are not fatal
        return self

    def recruited(self, answer):
        """
        The agency answered a recruitment request
        """
        # hold on to the answer for the request that is waiting for it
        self.answer = answer
        # all done
        return self

    def exited(self, report):
        """
        The agency reports that a member is gone; tell the recruiters that are waiting
        """
        # file the report
        self.exits[report.pid] = report.status
        # get the journal
        import journal

        # say what the agency reported
        journal.debug("pyre.nexus.staffing").log(
            f"the agency reports member {report.pid} gone, "
            f"status {os.waitstatus_to_exitcode(report.status)}"
        )
        # go through the subscribers
        for call in list(self.subscribers):
            # and if one is no longer interested
            if not call():
                # drop it
                self.subscribers.remove(call)
        # all done
        return self

    # event handlers
    def report(self, channel, **kwds):
        """
        The agency has reported an exit on the report channel; hear it

        Nothing else reads the report channel, but the readiness that woke me was recorded at the
        start of a pass of the event loop, and a reader on another event loop, e.g. one nested in
        a handler that ran earlier in the pass, may have taken delivery since; so i hear only what
        is still waiting

        N.B.: this is an event handler; returning a false value stops it
        """
        # if the agency has nothing left to say
        if not self.reports.pending():
            # keep listening for what it says next
            return True
        # otherwise, carefully, since the agency may be gone
        try:
            # hear it
            self.hear(channel=self.reports)
        # if the channel ended
        except EndOfStream:
            # the agency is gone; its members keep working, since they never talk to it, and the
            # next recruitment spawns a new one, which forgets this channel on every event loop
            return False
        # keep listening
        return True

    def overhear(self, channel, **kwds):
        """
        Replay the journal entries of the agency itself, as they arrive

        N.B.: this is an event handler; returning a false value stops it
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
            return False
        # an empty read means the agency is gone
        if not data:
            # so stop listening
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

    # implementation details
    def spawn(self) -> "Liaison":
        """
        Spawn the agency from the command line of the application, in my shell, handing it its
        ends of the control channel, of the report channel, and of the channel its journal
        entries come back over
        """
        # if there was an agency before, let go of my ends of its channels
        for channel in (self.control, self.reports, self.journal):
            # unless there was none
            if channel is None:
                # in which case there is nothing to let go of
                continue
            # the event loops that listened must forget it first, so nothing is left behind
            # under a descriptor number that is about to be recycled
            for dispatcher in self.listening:
                # one at a time
                dispatcher.forget(channel=channel)
            # then close it
            channel.close()
        # the control channel
        control = SocketPair.open()
        # the report channel
        reports = SocketPair.open()
        # and the journal channel
        journal = SocketPair.open()
        # channels cross to the agency on its command line, the way the channel schema renders
        # them
        schema = pyre.schemata.channel()
        # the command line of the agency: the application's own, in my shell
        argv = StaffingAgency.command + [
            # select the shell
            f"--shell={self.shell}",
            # hand it its end of the control channel
            f"--shell.control={schema.string(control.child)}",
            # of the report channel
            f"--shell.reports={schema.string(reports.child)}",
            # and of the channel its journal goes down
            f"--shell.journal={schema.string(journal.child)}",
        ]
        # the descriptors of its ends, which it inherits under the same numbers
        inherited = (
            control.child.descriptors() + reports.child.descriptors() + journal.child.descriptors()
        )
        # spawn it, with the same environment and working directory
        self.process = subprocess.Popen(argv, pass_fds=inherited, close_fds=True)
        # its ends are its own now, so release my copies
        control.child.close()
        # all of them
        reports.child.close()
        journal.child.close()
        # keep mine
        self.control = control.parent
        self.reports = reports.parent
        self.journal = journal.parent
        # nothing has been heard from it yet
        self.exits = {}
        self.tail = b""
        # and no event loop listens to it yet
        self.listening.clear()
        # the first thing the agency says is what it runs
        self.hear(channel=self.control)
        # get the journal
        import journal

        # and say that it is up
        journal.debug("pyre.nexus.staffing").log(
            f"spawned the staffing agency, pid {self.process.pid}"
        )
        # all done
        return self

    def listen(self, dispatcher) -> "Liaison":
        """
        Hear the agency's reports and journal entries on {dispatcher}, unless they are heard
        there already
        """
        # if they are
        if dispatcher in self.listening:
            # there is nothing to do
            return self
        # mark it
        self.listening.add(dispatcher)
        # hear the reports
        dispatcher.whenReadReady(channel=self.reports, call=self.report)
        # and the journal entries
        dispatcher.whenReadReady(channel=self.journal, call=self.overhear)
        # all done
        return self

    def hear(self, channel) -> "Liaison":
        """
        Take delivery of the next message from the agency on {channel}, and handle it
        """
        # get it
        message = Message.receive(channel=channel, marshaler=self.marshaler)
        # and handle it
        message.deliver(recipient=self)
        # all done
        return self

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the agency's process, once spawned
        self.process = None
        # my ends of the control channel, of the report channel, and of the agency's journal
        # channel
        self.control = None
        self.reports = None
        self.journal = None
        # the exits the agency reported that nobody has collected yet, by pid
        self.exits = {}
        # the answer to the recruitment request in flight
        self.answer = None
        # the start of a journal record still in transit
        self.tail = b""
        # the recruiters waiting to hear of exits
        self.subscribers = []
        # and the event loops that hear the agency
        self.listening = set()
        # all done
        return


# end of file
