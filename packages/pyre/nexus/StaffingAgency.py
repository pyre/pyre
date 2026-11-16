# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import signal
import sys
import traceback

# support
import journal
import pyre

# the marker the marshaler raises when its peer goes away
from ..ipc.exceptions import EndOfStream

# the base class of the members, which knows how they route their journal
from .Crew import Crew

# what the agency says
from .messages.Message import Message
from .messages.Greeting import Greeting
from .messages.Recruited import Recruited
from .messages.Exited import Exited


# declaration
class StaffingAgency(pyre.component, family="pyre.nexus.agencies.staffing"):
    """
    A clean copy of the application that forks crew members for the teams of the process that
    started it

    The agency is spawned, not forked, from the command line of the application, so it runs the
    same code under the same configuration, but it never does anything but serve requests: the
    members it forks are copies of a process that has touched nothing, whatever the process
    that asks for them has touched since it started. It serves on an event loop of its own:
    requests arrive on the control channel and are answered there, the exits of its members
    arrive through {SIGCHLD} and are reported on the report channel, and the end of the control
    channel, which is how the process that started it lets go, ends the loop
    """

    # user configurable state
    marshaler = pyre.ipc.marshaler()
    marshaler.doc = "the serializer of the messages on the control and report channels"

    # the event loop i serve on
    dispatcher = pyre.ipc.dispatcher()
    dispatcher.doc = "the manager of my event loop"

    # interface
    @classmethod
    def fingerprint(cls) -> dict:
        """
        Describe what this process runs, so an agency can prove it runs the same thing as the
        process that started it
        """
        # the pieces that must agree
        return {
            # the interpreter
            "executable": os.path.realpath(sys.executable),
            # the installation of the framework
            "pyre": os.path.realpath(pyre.__file__),
            # the interpreter options and the script; the arguments that follow are the same by
            # construction, except for the ones that select the agency's shell
            "script": cls.script,
        }

    def serve(self, control, reports, journal=None) -> int:
        """
        Serve the requests arriving on the {control} channel until the process that started me
        lets go; the exits of my members are reported down the {reports} channel, and my own
        journal entries go down the {journal} channel
        """
        # the interrupt key reaches the whole process group, but i leave when my parent does
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # hold on to the control channel
        self.channel = control
        # and the report channel
        self.reports = reports
        # if my journal is to be routed
        if journal is not None:
            # hold on to its channel
            self.journal = journal
            # and ship it
            self.device = self.ship(channel=journal)
        # say what i am running
        Greeting(fingerprint=self.fingerprint()).send(
            channel=self.channel, marshaler=self.marshaler
        )
        # hear the requests
        self.dispatcher.whenReadReady(channel=self.channel, call=self.request)
        # and the exits of my members
        self.dispatcher.whenSignal(signal=signal.SIGCHLD, call=self.harvest)
        # serve until the control channel ends
        self.dispatcher.watch()
        # all done
        return 0

    # message handlers
    def recruit(self, request):
        """
        Fork the members described by {request}, one after the other, and answer with their pids
        """
        # the ends of the channels of each member
        members = list(request.members())
        # fork them, handing each one the ends of the members forked after it, which it inherits
        # and must release
        pids = [
            self.enlist(request=request, ends=ends, others=members[index + 1 :])
            for index, ends in enumerate(members)
        ]
        # and say who they are
        Recruited(pids=pids).send(channel=self.channel, marshaler=self.marshaler)
        # all done
        return self

    def instruct(self, order):
        """
        Apply the journal control in {order}, so the members i fork from now on start with it in
        place
        """
        # get the wire form of controls
        from journal import control as Control

        # apply it here
        Control.decode(order.control).apply()
        # all done
        return self

    # event handlers
    def request(self, channel, **kwds):
        """
        A request has arrived on the control channel; serve it

        N.B.: this is an event handler; returning a false value stops it
        """
        # carefully, since the process that started me may be gone
        try:
            # get the request
            message = Message.receive(channel=channel, marshaler=self.marshaler)
        # if the channel ended
        except EndOfStream:
            # i have nobody left to serve
            self.dispatcher.stop()
            # so stop listening
            return False
        # serve it
        message.deliver(recipient=self)
        # and keep listening
        return True

    def harvest(self, **kwds):
        """
        Some of my members may have left: collect them, and report each one

        N.B.: this is an event handler; returning a false value stops it
        """
        # as long as there are any
        while True:
            # carefully
            try:
                # ask, without waiting; every child of mine is a member
                pid, status = os.waitpid(-1, os.WNOHANG)
            # with no children at all
            except ChildProcessError:
                # there is nothing to collect
                break
            # with none that exited
            if pid == 0:
                # there is nothing to collect either
                break
            # say so
            journal.debug("pyre.nexus.staffing").log(f"agency: reaped member {pid}")
            # and report the one that did
            Exited(pid=pid, status=status).send(channel=self.reports, marshaler=self.marshaler)
        # keep listening
        return True

    # implementation details
    def enlist(self, request, ends, others):
        """
        Fork a new crew member of the class in {request}, with the channel {ends} it talks to its
        team over; {others} are the ends of the members of the same request yet to be forked
        """
        # fork
        pid = os.fork()
        # on my side
        if pid > 0:
            # the member's channels belong to the member now
            for channel in ends:
                # so release my copies
                if channel is not None:
                    # one at a time
                    channel.close()
            # say so
            journal.debug("pyre.nexus.staffing").log(f"agency: forked member {pid}")
            # and hand back its pid
            return pid
        # in the member: whatever happens from here on, this process must never return into my
        # event loop
        try:
            # become the member; this does not return
            self.member(request=request, ends=ends, others=others)
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

    def member(self, request, ends, others):
        """
        Turn this fresh fork of mine into a crew member of the class in {request}, with the
        channel {ends} it talks to its team over, letting go of the ends of the {others}
        """
        # the control channel is my business
        self.channel.close()
        # and so is the report channel
        self.reports.close()
        # the ends of the members forked after this one belong to them
        for channels in others:
            # all of them
            for channel in channels:
                # that exist
                if channel is not None:
                    # release my copy
                    channel.close()
        # and so is my journal
        if self.device is not None:
            # release the device that ships it
            self.device.close()
            # and the channel it travels over
            self.journal.close()
            # and leave the member with the console until it routes its own journal
            from journal import chronicler, cout

            # install it
            chronicler.device = cout()
        # the member's channels came with the request
        channel, journal = ends
        # route the member's journal to the team first, so whatever goes wrong from here on,
        # starting with loading its class, is heard there
        courier = Crew.route(channel=journal)
        # load the class of the member; this imports its module, here, after the fork
        crew = request.load()(pid=os.getpid(), channel=channel, journal=journal)
        # which keeps the device that ships its journal alive for as long as it lives
        crew.courier = courier
        # ask it to register with the team
        crew.register()
        # and put it to work; this does not return
        crew.work()

    def ship(self, channel):
        """
        Send everything this process says to the journal down {channel}
        """
        # get the journal
        import journal

        # and the device that ships its entries down a channel; it is built on the journal, which
        # may still be booting when this module is first imported
        from ..ipc.Courier import Courier

        # make the device
        device = Courier(channel=channel)
        # install it
        journal.chronicler.device = device
        # and hand it off
        return device

    @staticmethod
    def invocation():
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

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the control channel, while i serve
        self.channel = None
        # the channel my reports of exits travel over, while i serve
        self.reports = None
        # the channel my journal travels over, if it is routed
        self.journal = None
        # and the device that ships it
        self.device = None
        # all done
        return

    # the command line of this process, captured when the class is defined, before anybody has a
    # chance to change the working directory, so the agency runs the same script
    command = invocation()
    # the part of it that names the interpreter, its options, and the script
    script = command[: len(command) - len(sys.argv) + 1]


# end of file
