# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import functools
import os
import signal
import sys
import time

# support
import pyre
from ..units.SI import second

# my protocol
from .Recruiter import Recruiter

# the record of a member on its way out
from .Departure import Departure


# declaration
class Fork(pyre.component, family="pyre.nexus.recruiters.fork", implements=Recruiter):
    """
    Create worker processes by cloning the current one

    New team members inherit only what they need: each side of the crew channel closes the end
    it does not own, so a worker sees end-of-file when the team dies instead of lingering on a
    channel its own inherited copies hold open; and workers shed everything else the fork
    handed them that is none of their business, i.e. whatever the shared event loop watches
    and the channels of the crews deployed before them

    Members leave without anybody waiting for them: a dismissed member goes on a ledger of
    departures, its exit arrives as an event on the event loop of its team, and a single alarm
    reminds the ones that are late, so a team that sends many members home at once pays for
    none of their exits
    """

    # user configurable state
    channels = pyre.ipc.transport()
    channels.doc = "the ipc mechanism that connects the team to its crew members"

    # whether the members talk back
    journal = pyre.properties.bool(default=True)
    journal.doc = "whether the journal entries of each crew member are routed back to the team"

    # how patient i am with a member on its way out
    grace = pyre.properties.dimensional(default=2 * second)
    grace.doc = "how long a dismissed crew member gets to leave before it is made to"

    # protocol obligations
    @pyre.export
    def recruit(self, team, **kwds):
        """
        Recruit members for the {team}
        """
        # compute the number of vacancies in the team
        vacancies = team.vacancies()
        # recruit the right number of team members
        for _ in range(vacancies):
            # deploy them and add them to the team
            yield self.deploy(team=team, **kwds)
        # all done
        return

    @pyre.export
    def deploy(self, team, **kwds):
        """
        Create a new {team} member using the {fork} system call
        """
        # team members communicate with the manager over my transport; the {child} end is
        # destined for the worker, the {parent} end stays with the team
        parent, child = self.channels.open()
        # the worker's journal entries travel back over a channel of their own, when wanted;
        # the crew channel carries a protocol of its own, and a diagnostic must never have to
        # wait for a report to be due
        parentJournal, childJournal = self.channels.open() if self.journal else (None, None)
        # clone the current process
        pid = os.fork()

        # N.B.: it is important that the worker side of a new team member gets a fresh event
        # loop manager, while the team side is tied to the shared one.

        # in the worker process
        if pid == 0:
            # the interrupt key reaches the whole process group, but a worker is the team's to
            # manage: it leaves when the team lets go, so the interrupt is not for it, and
            # neither is the application's report that it was interrupted
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            # the team's end is not mine to hold; release my inherited copy so the channel
            # closes for real when the team side lets go
            parent.close()
            # and the same for the team's end of the journal channel, if there is one
            if parentJournal is not None:
                # release it
                parentJournal.close()
            # shed the rest of the connections the fork handed me
            self.shed(team=team)
            # make a team member
            crew = team.crew(pid=os.getpid(), channel=child, journal=childJournal, **kwds)
            # route its journal to the team, and have it keep the device that ships it alive
            crew.courier = crew.route(channel=childJournal)
            # ask it to register with the team
            crew.register()
            # and put it to work; this does not return
            crew.work()

        # on the team side, release the worker's end for the same reason
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

    @pyre.export
    def dismiss(self, team, crew, **kwds):
        """
        The {team} manager has dismissed the given {crew} member, which has been told to leave

        Nobody waits for it: it goes on my ledger of departures, and its team hears that it is
        gone once its process has left
        """
        # put it on the ledger
        return self.depart(team=team, crew=crew)

    @pyre.export
    def bury(self, team, crew, **kwds):
        """
        The {crew} member of {team} died without being dismissed

        A member whose channel closed may still be on its way out, so it is treated as a
        dismissed one: collected once its process is gone, and reminded if it lingers
        """
        # put it on the ledger
        return self.depart(team=team, crew=crew)

    @pyre.export
    def settle(self, team, **kwds):
        """
        Wait until every member on its way out is gone; for a {team} that is shutting down

        The team's own event loop may not be running any more, or may be the one that called
        me, so the departures are seen through on an event loop of their own, of the same kind
        """
        # if nobody is on the way out
        if not self.departures:
            # there is nothing to wait for
            return self
        # make an event loop like the team's
        loop = type(team.dispatcher)()
        # remember it, so it can be stopped once the ledger is empty
        self.settling = loop
        # hear the exits and keep the deadlines on it
        self.watch(dispatcher=loop)
        # run it, until the last departure is collected
        loop.watch()
        # forget it
        self.settling = None
        # and release its resources
        loop.close()
        # all done
        return self

    @pyre.export
    def instruct(self, control):
        """
        The journal {control} was applied to the team; members forked from its process from now
        on inherit it, so there is nothing to pass along
        """
        # nothing to do
        return

    # implementation details
    def depart(self, team, crew):
        """
        Put the {crew} member of {team} on my ledger of departures, due to be gone within my
        grace period, and see that its exit and its deadline are heard on its team's event loop
        """
        # the deadline
        deadline = time.monotonic() + self.grace / second
        # record the departure
        self.departures[crew.pid] = Departure(crew=crew, team=team, deadline=deadline)
        # a member that is gone already left before anybody was listening for it, so collect it
        # now rather than at its deadline
        self.collect()
        # if nobody is left on the ledger
        if not self.departures:
            # there is nothing to watch over
            return self
        # otherwise, watch over the departures on the team's event loop
        return self.watch(dispatcher=team.dispatcher)

    def watch(self, dispatcher):
        """
        Arrange for the exits of departing members to be heard, and their deadlines kept, on
        {dispatcher}
        """
        # hear the exits there, unless i already do
        if dispatcher not in self.listening:
            # mark it
            self.listening.add(dispatcher)
            # and listen
            self.listen(dispatcher=dispatcher)
        # keep the deadlines there, unless i already do
        if dispatcher not in self.reminding:
            # mark it
            self.reminding.add(dispatcher)
            # the earliest deadline is no further than a grace period away
            dispatcher.alarm(
                interval=self.grace, call=functools.partial(self.remind, dispatcher=dispatcher)
            )
        # all done
        return self

    def listen(self, dispatcher):
        """
        Hear the exits of my members on {dispatcher}: they are children of this process, which
        is told of each exit through {SIGCHLD}
        """
        # the relay delivers the signal to the event loop
        dispatcher.whenSignal(signal=signal.SIGCHLD, call=self.exited)
        # all done
        return self

    def exited(self, **kwds):
        """
        Some members may have left: collect the ones that did, and keep listening for as long
        as anybody is still on the way out

        N.B.: this is an event handler; returning a false value stops it
        """
        # collect
        self.collect()
        # if the ledger is empty
        if not self.departures:
            # nobody is listening any more, on any event loop
            self.listening.clear()
            # so stop
            return False
        # otherwise, keep listening
        return True

    def collect(self):
        """
        Take the members that are gone off my ledger, and tell their teams
        """
        # get the journal
        import journal

        # make a channel
        channel = journal.debug("pyre.nexus.departures")
        # go through the departures
        for pid in list(self.departures):
            # check on each one
            gone, status = self.reap(pid=pid)
            # if it is still around
            if not gone:
                # leave it on the ledger
                continue
            # otherwise, take it off
            departure = self.departures.pop(pid)
            # its exit code, when its status was collected
            code = "unknown" if status is None else os.waitstatus_to_exitcode(status)
            # say how it left
            channel.log(f"{departure.team.pyre_name}: member {pid} is gone, status {code}")
            # and let its team know
            departure.team.departed(crew=departure.crew, status=status)
        # if a team is settling and the ledger is empty
        if self.settling is not None and not self.departures:
            # its wait is over
            self.settling.stop()
        # all done
        return self

    def reap(self, pid):
        """
        Check, without waiting, whether my child {pid} is gone; report whether it is, and its
        exit status
        """
        # carefully
        try:
            # harvest it if it left
            child, status = os.waitpid(pid, os.WNOHANG)
        # a child that somebody else already harvested
        except ChildProcessError:
            # is just as gone, with no status to report
            return True, None
        # a child that left comes back under its own pid
        return child == pid, status

    def remind(self, timestamp, dispatcher):
        """
        A deadline has come: collect the members that left, remind the ones that are late, and
        come back at the next deadline

        N.B.: this is an alarm handler; it returns the time until it is next due, or {None} once
        the ledger is empty
        """
        # collect whoever left
        self.collect()
        # if the ledger is empty
        if not self.departures:
            # nothing is kept on {dispatcher} any more
            self.reminding.discard(dispatcher)
            # and the alarm stops
            return None
        # the time now
        now = time.monotonic()
        # and the grace period, in seconds
        grace = self.grace / second
        # go through the departures
        for departure in self.departures.values():
            # if this one is late
            if departure.due(now=now):
                # remind it
                departure.remind(now=now, grace=grace)
        # the next deadline
        deadline = min(departure.deadline for departure in self.departures.values())
        # is when the alarm comes back
        return (deadline - now) * second

    def shed(self, team):
        """
        Close the inherited connections that belong to the {team} side, not to a new crew
        member

        The parent's open data files are left alone deliberately: closing their descriptors
        out from under the inherited objects that will finalize them invites descriptor reuse
        bugs, and holding them is harmless
        """
        # collect the channels the shared event loop is watching
        pile = set(team.dispatcher.channels())
        # add the channels of every deployed crew; members between tasks may have no armed
        # handler, so the event loop does not know about them
        pile |= set(crew.channel for crew in team.crews())
        # and the team's ends of their journal channels
        pile |= set(crew.journal for crew in team.crews() if crew.journal is not None)
        # go through the pile
        for channel in pile:
            # carefully, since a descriptor may already be gone
            try:
                # release my inherited copy
                channel.close()
            # dead ones
            except OSError:
                # need nothing further
                continue
        # all done
        return

    # framework notifications
    @classmethod
    def pyre_classInitialized(cls):
        """
        Keep the parent side of a fork away from the macOS system configuration, as soon as the
        recruiter exists, which is as early as it gets for a process that means to fork
        """
        # shield the process
        cls.shield()
        # and chain up
        return super().pyre_classInitialized()

    @classmethod
    def shield(cls):
        """
        Make the standard library look for proxy settings in the environment only, the way it
        does on every other platform, and never in the macOS system configuration

        That lookup goes through {_scproxy}, which brings CoreFoundation to life in this process.
        CoreFoundation and the dispatch queues underneath it do not survive a fork that is not
        followed by an exec, and a crew member is exactly such a fork. The member need not look
        for proxies itself to get hurt: anything in it that reaches CoreFoundation will do, e.g.
        the TLS layer of the AWS libraries that hdf5 reads S3 with, which is built on Secure
        Transport; the member dies of a segmentation fault while setting up its first
        connection. All it takes on the team side is one http client asking whether there is a
        proxy, which {boto3} does while it builds a session

        The lookup functions in {urllib.request} resolve {_get_proxies} and
        {_get_proxy_settings} as globals of that module when they are called, so replacing
        those two names reaches every caller, including the ones that captured the lookup
        functions themselves before this ran, as {botocore} does when it is imported
        """
        # this is a problem of one platform
        if sys.platform != "darwin":
            # and everybody else is fine
            return
        # get the module with the lookup functions
        import urllib.request

        # there are no proxies in the system configuration
        urllib.request._get_proxies = lambda: {}
        # and nothing there says which hosts bypass them
        urllib.request._get_proxy_settings = lambda: {"exclude_simple": False, "exceptions": ()}
        # all done
        return

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the members on their way out, by pid
        self.departures = {}
        # the event loops that hear the exits of departing members
        self.listening = set()
        # and the ones that keep their deadlines
        self.reminding = set()
        # the event loop of a team that is waiting for its departures, while it waits
        self.settling = None
        # all done
        return


# end of file
