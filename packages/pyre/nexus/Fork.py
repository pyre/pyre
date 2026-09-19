# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import signal
import sys
import time
import traceback

# support
import pyre
from ..units.SI import second

# my protocol
from .Recruiter import Recruiter


# keep the parent side of a fork away from the macOS system configuration
def shield():
    """
    Make the standard library look for proxy settings in the environment only, the way it does
    on every other platform, and never in the macOS system configuration

    That lookup goes through {_scproxy}, which brings CoreFoundation to life in this process.
    CoreFoundation and the dispatch queues underneath it do not survive a fork that is not
    followed by an exec, and a crew member is exactly such a fork. The member need not look
    for proxies itself to get hurt: anything in it that reaches CoreFoundation will do, e.g.
    the TLS layer of the AWS libraries that hdf5 reads S3 with, which is built on Secure
    Transport; the member dies of a segmentation fault while setting up its first connection.
    All it takes on the team side is one http client asking whether there is a proxy, which
    {boto3} does while it builds a session

    The lookup functions in {urllib.request} resolve {_get_proxies} and {_get_proxy_settings}
    as globals of that module when they are called, so replacing those two names reaches every
    caller, including the ones that captured the lookup functions themselves before this ran,
    as {botocore} does when it is imported. That makes the order of imports irrelevant; what
    matters is that this happens before the first lookup, and importing the recruiter that
    forks is as early as it gets for a process that means to fork
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


# this happens once, when the recruiter is imported
shield()


# declaration
class Fork(pyre.component, family="pyre.nexus.recruiters.fork", implements=Recruiter):
    """
    Create worker processes by cloning the current one

    New team members inherit only what they need: each side of the crew channel closes the end
    it does not own, so a worker sees end-of-file when the team dies instead of lingering on a
    channel its own inherited copies hold open; and workers shed everything else the fork
    handed them that is none of their business, i.e. whatever the shared event loop watches
    and the channels of the crews deployed before them
    """

    # user configurable state
    channels = pyre.ipc.transport()
    channels.doc = "the ipc mechanism that connects the team to its crew members"

    journal = pyre.properties.bool(default=True)
    journal.doc = "whether the journal entries of each crew member are routed back to the team"

    grace = pyre.properties.dimensional(default=2 * second)
    grace.doc = "how long a dismissed crew member gets to leave before it is made to"

    # protocol obligations
    @pyre.provides
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

    @pyre.provides
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
            # if my journal is routed to the team
            if childJournal is not None:
                # install the device that ships it, and keep it alive for as long as i am
                crew.courier = self.route(channel=childJournal)
            # ask it to register with the team
            crew.register()
            # assume the worst, so that anything that goes wrong is reported as a failure
            status = 1
            # and keep track of whether the member got to finish; asking the interpreter
            # whether an exception is in flight does not work here: a replacement member is
            # forked from within the handler of the failure of the one it replaces, so it
            # inherits an exception that is the team's business, not its own
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

    @pyre.provides
    def dismiss(self, team, crew, **kwds):
        """
        The {team} manager has dismissed the given {member}

        The member is expected to leave on its own, and gets a grace period to do so. One that
        is still around when the period is over is told to go, and one that ignores that is
        removed: a team must never wait forever on a member, since the team lives in the
        process that serves everybody else, and a member stuck on its way out, e.g. in an
        exit handler that waits for a thread that does not exist on its side of the fork,
        would otherwise hold that process, and whatever ports it has open, hostage
        """
        # get the process id of the member
        pid = crew.pid
        # and the grace period, in seconds
        grace = self.grace / second
        # give it a chance to leave on its own
        if self.reap(pid=pid, patience=grace):
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
            if self.reap(pid=pid, patience=grace):
                # it left
                return
        # nothing survives the last reminder, so this cannot block for long
        self.reap(pid=pid, patience=None)
        # all done
        return

    # implementation details
    def reap(self, pid, patience):
        """
        Harvest the exit status of the child {pid}, waiting up to {patience} seconds for it to
        leave; with no {patience}, wait for as long as it takes. Report whether it is gone
        """
        # with no deadline
        if patience is None:
            # carefully
            try:
                # wait for as long as it takes
                os.waitpid(pid, 0)
            # a child that somebody else already harvested
            except ChildProcessError:
                # is just as gone
                pass
            # either way
            return True
        # otherwise, set the deadline
        deadline = time.monotonic() + patience
        # and keep checking
        while True:
            # carefully
            try:
                # ask, without waiting
                gone, _ = os.waitpid(pid, os.WNOHANG)
            # a child that somebody else already harvested
            except ChildProcessError:
                # is just as gone
                return True
            # if it left
            if gone:
                # we are done
                return True
            # if time is up
            if time.monotonic() >= deadline:
                # it is still here
                return False
            # otherwise, check back soon
            time.sleep(0.01)

    def leave(self, crew, status, crashed=False):
        """
        End the process of a {crew} member with the given exit {status}; {crashed} says that
        the member is on its way out because of an exception nobody handled

        A crew member is a fork of the team's process, so the exit handlers it would run on
        the way out are the team's: registered by libraries in a process that had state the
        member does not share, e.g. threads, which do not survive a fork. Such a handler may
        wait forever for something that exists only on the other side of the fork, and then
        the member never leaves. So the member ends its process directly, after putting its
        own affairs in order, and the inherited handlers never run
        """
        # if i got here because something went wrong that nobody handled
        if crashed:
            # say what it was, since the interpreter will not get the chance
            traceback.print_exc()
        # carefully, since nothing must get in the way of leaving
        try:
            # let the member put its affairs in order, e.g. close what it has open for writing
            crew.retire()
        # and whatever happens
        finally:
            # go through the standard streams
            for stream in (sys.stdout, sys.stderr):
                # carefully, since they may be closed or broken
                try:
                    # deliver what is pending; nothing else will
                    stream.flush()
                # if that fails
                except (OSError, ValueError):
                    # there is nothing to be done about it
                    pass
            # normalize the status the way the interpreter does: nothing means success, a
            # number is itself, and anything else is a failure
            code = 0 if status is None else status if isinstance(status, int) else 1
            # and end the process without running the exit handlers
            os._exit(code)

    # implementation details
    def route(self, channel):
        """
        Send everything this process says to the journal down {channel}, for the team to hear
        """
        # get the journal
        import journal

        # the writable end of the channel; a socket is its own end, a pipe hands out a descriptor
        end = channel.outbound
        # get the descriptor
        descriptor = end.fileno() if hasattr(end, "fileno") else end
        # make the device; the terminal is left to the team, which replays every entry it
        # hears, so there is nothing to mirror
        courier = journal.courier(descriptor=descriptor)
        # install it
        journal.chronicler.device = courier
        # and hand it to the caller, whose reference keeps it alive
        return courier

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


# end of file
