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

    The liaison spawns the agency from the command line of the application, holds this side of
    the control channel, sends the recruitment requests and the journal controls, and turns the
    agency's reports of exits into events on the event loops of the teams. There is one per
    process, reached by name, so every recruiter that uses the agency uses the same one
    """

    # user configurable state
    shell = pyre.properties.str(default="forkserver")
    shell.doc = "the shell that turns a copy of the application into the staffing agency"

    # how the messages on the control channel are encoded
    marshaler = pyre.ipc.marshaler()
    marshaler.doc = "the serializer of the messages on the control channel"

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

    def recruit(self, request) -> int:
        """
        Send the recruitment {request} and wait for the pid of the member; the answer is a local
        round trip, so recruitment stays synchronous
        """
        # no answer yet
        self.answer = None
        # send the request
        request.send(channel=self.control, marshaler=self.marshaler)
        # take delivery of what the agency says until the answer is in
        while self.answer is None:
            # one message at a time
            self.hear()
        # get the journal
        import journal

        # say who it is
        journal.debug("pyre.nexus.staffing").log(f"the agency recruited member {self.answer.pid}")
        # and hand off the pid
        return self.answer.pid

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
        The agency has something to say on the control channel; hear it

        N.B.: this is an event handler; returning a false value stops it
        """
        # carefully, since the agency may be gone
        try:
            # hear it
            self.hear()
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
        ends of the control channel and of the channel its journal entries come back over
        """
        # if there was an agency before, let go of my ends of its channels
        for channel in (self.control, self.journal):
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
        # and the journal channel
        journal = SocketPair.open()
        # the command line of the agency: the application's own, in my shell
        argv = StaffingAgency.command + [
            # select the shell
            f"--shell={self.shell}",
            # tell it where the control channel is
            f"--shell.control={control.child.fileno()}",
            # and where its journal goes
            f"--shell.journal={journal.child.fileno()}",
        ]
        # spawn it, with the same environment and working directory, handing it its two ends
        self.process = subprocess.Popen(
            argv, pass_fds=(control.child.fileno(), journal.child.fileno()), close_fds=True
        )
        # its ends are its own now
        control.child.close()
        # both of them
        journal.child.close()
        # keep mine
        self.control = control.parent
        self.journal = journal.parent
        # nothing has been heard from it yet
        self.exits = {}
        self.tail = b""
        # and no event loop listens to it yet
        self.listening.clear()
        # the first thing the agency says is what it runs
        self.hear()
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
        dispatcher.whenReadReady(channel=self.control, call=self.report)
        # and the journal entries
        dispatcher.whenReadReady(channel=self.journal, call=self.overhear)
        # all done
        return self

    def hear(self) -> "Liaison":
        """
        Take delivery of the next message from the agency, and handle it
        """
        # get it
        message = Message.receive(channel=self.control, marshaler=self.marshaler)
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
        # my ends of the control channel and of the agency's journal channel
        self.control = None
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
