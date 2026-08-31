# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import atexit
import functools
import os
import signal

# support
import pyre
import journal

# the unit the task deadline is expressed in
from ..units.SI import second

# my base class
from .Pool import Pool


# declaration
class Staff(Pool, family="pyre.nexus.teams.staff"):
    """
    A standing team of persistent worker processes in the service of a long lived application

    Unlike a {Pool}, which drafts workers for a workplan and dismisses them when it drains,
    a {Staff} keeps its crew members around: idle ones are parked and woken when new work
    arrives, casualties are noticed and replaced, and task outcomes are delivered to per-task
    callbacks instead of being logged and discarded. Task failures are not retried: the
    outcome, good or bad, goes to the callback, and retry policy belongs to the client
    """

    # types
    # the marker for failures the client can recover from by asking again
    from .exceptions import RecoverableError

    # user configurable state
    patience = pyre.properties.dimensional(default=0 * second)
    patience.doc = "how long a task may take before its crew member is presumed lost"

    # interface
    def assign(self, task, callback):
        """
        Queue {task} for execution and arrange for {callback} to receive the outcome

        The callback is invoked with {result} and {error} keyword arguments, exactly one of
        which is non-trivial. Tasks that compare equal are executed once: later requests
        join the standing one, and every callback receives the shared outcome. A repeated
        request also renews the task's priority, since work is served newest first
        """
        # a disbanded staff serves nobody
        if self._disbanded:
            # so let the caller down right away
            callback(result=None, error=self.RecoverableError(description="staff disbanded"))
            # all done
            return self
        # look for a standing request for the same work
        callbacks = self.pending.get(task)
        # if there is one
        if callbacks is not None:
            # join it
            callbacks.append(callback)
            # if the task is still waiting for a crew member
            if task in self.workplan:
                # renew its priority: work is served newest first
                del self.workplan[task]
                self.workplan[task] = None
            # either way, the standing request covers this one
            return self
        # otherwise, open the callback ledger for this task
        self.pending[task] = [callback]
        # add the task to the workplan
        self.workplan[task] = None
        # and mobilize: recruit up to strength and wake the bench
        self.assemble(workplan=())
        # all done
        return self

    def revoke(self, task, callback):
        """
        Withdraw {callback} from the outcome of {task}, e.g. because its requester went away

        When the last interested party withdraws from a task that has not yet been picked up,
        the task itself is dropped; work already in a crew member's hands runs to completion,
        and its outcome is quietly discarded
        """
        # look up the callback ledger
        callbacks = self.pending.get(task)
        # if there is no standing request, or this callback is not part of it
        if callbacks is None or callback not in callbacks:
            # there is nothing to withdraw
            return self
        # take the callback out
        callbacks.remove(callback)
        # if nobody is left waiting and the task is still queued
        if not callbacks and task in self.workplan:
            # drop the task
            del self.workplan[task]
            # and close its ledger
            del self.pending[task]
        # all done
        return self

    def crews(self):
        """
        Generate every current crew member, whatever its state
        """
        # chain up for the ones checking in and the ones on a task
        yield from super().crews()
        # and add the ones parked on the bench
        yield from self.idle
        # all done
        return

    def recover(self, **kwds):
        """
        Restore the staff to full strength after a casualty
        """
        # a disbanded staff stays disbanded; a recovery must not resurrect it
        if self._disbanded:
            # so it does nothing
            return None
        # otherwise, recruit replacements and wake the bench, in case there is work waiting
        self.assemble(workplan=set())
        # all done
        return None

    def disband(self):
        """
        Dismiss every crew member; invoked at shutdown so no workers are orphaned
        """
        # crew dismissal is a team side activity; forked children that inherited my atexit
        # registration must not attempt it
        if os.getpid() != self._manager:
            # so they bail
            return self
        # mark me, so a recovery arriving after this moment cannot resurrect me
        self._disbanded = True
        # the parked and still-checking-in members are between tasks and exit on request
        resting = set(self.idle) | set(self.registered)
        # members that are mid-task would block writing a report nobody will drain, so a
        # graceful dismissal can deadlock the exit; they get terminated instead
        working = set(self.active)
        # empty the rosters
        self.idle.clear()
        self.active.clear()
        self.registered.clear()
        self.vigils.clear()
        # go through the resting members
        for crew in resting:
            # carefully, since a member may have died on its own
            try:
                # ask each one to exit
                crew.dismissed()
                # and reap the process
                self.recruiter.dismiss(team=self, crew=crew)
            # dead members raise while being messaged or waited on
            except (OSError, ChildProcessError):
                # nothing more to do for them
                continue
        # go through the working members
        for crew in working:
            # carefully, for the same reason
            try:
                # terminate each one; its work is moot at exit
                os.kill(crew.pid, signal.SIGKILL)
                # and reap the process
                os.waitpid(crew.pid, 0)
            # dead members raise while being signaled or waited on
            except (OSError, ChildProcessError):
                # nothing more to do for them
                continue
        # tasks still awaiting outcomes will never get one; deliver the bad news so nobody
        # is left waiting on a promise
        for task, callbacks in list(self.pending.items()):
            # go through the subscribers
            for callback in callbacks:
                # and let each one down gently
                callback(
                    result=None,
                    error=self.RecoverableError(description="staff disbanded"),
                )
        # and clear the ledger
        self.pending.clear()
        # all done
        return self

    # team protocol obligations
    @pyre.export
    def assemble(self, workplan, **kwds):
        """
        Add the tasks in {workplan} to my schedule
        """
        # go through the incoming tasks
        for task in workplan:
            # and extend the workplan; reinsertion renews a queued task's priority
            self.workplan[task] = None
        # recruit up to full strength
        self.recruit()
        # if there is work to do
        if self.workplan:
            # wake the parked crew members; extras just go back to the bench
            while self.idle:
                # take each one off the bench
                crew = self.idle.pop()
                # return it to duty
                self.active.add(crew)
                # and put it back on the schedule
                self.schedule(crew=crew)
        # all done
        return self

    @pyre.export
    def vacancies(self):
        """
        Compute how many recruits are needed to take the staff to full strength
        """
        # my crew members are persistent, so aim for full strength regardless of backlog;
        # everybody counts: the ones checking in, the ones on a task, and the parked ones
        return self.size - len(self.registered) - len(self.active) - len(self.idle)

    # outcome hooks, invoked by crew members as they harvest completion reports
    def collect(self, task, result):
        """
        A crew member has delivered the {result} of {task}
        """
        # look up the callback ledger
        callbacks = self.pending.pop(task, None)
        # a missing ledger means the task outcome was already delivered; it's a bug
        if callbacks is None:
            # build a channel
            firewall = journal.firewall("pyre.nexus.staff")
            # complain
            firewall.line(f"duplicate delivery for {task}")
            firewall.line(f"while collecting a result in {self}")
            # flush
            firewall.log()
            # and bail, in case firewalls aren't fatal
            return self
        # go through the subscribers; an empty ledger means every interested party withdrew,
        # and the result is quietly discarded
        for callback in callbacks:
            # hand each one the result
            callback(result=result, error=None)
        # all done
        return self

    def requeue(self, task, error):
        """
        A crew member reports that {task} failed with a recoverable {error}
        """
        # a staff does not retry: the client owns retry policy, so even a recoverable
        # failure is an outcome to deliver
        return self.abandon(task=task, error=error)

    def abandon(self, task, error):
        """
        A crew member reports that {task} is lost to {error}
        """
        # look up the callback ledger
        callbacks = self.pending.pop(task, None)
        # a missing ledger means the task outcome was already delivered; it's a bug
        if callbacks is None:
            # build a channel
            firewall = journal.firewall("pyre.nexus.staff")
            # complain
            firewall.line(f"duplicate abandonment for {task}: {error}")
            firewall.line(f"while delivering bad news in {self}")
            # flush
            firewall.log()
            # and bail, in case firewalls aren't fatal
            return self
        # go through the subscribers, if any are left
        for callback in callbacks:
            # and hand each one the bad news
            callback(result=None, error=error)
        # all done
        return self

    def bury(self, crew):
        """
        A {crew} member died without a formal dismissal; clean up after it and restore the
        staff to full strength
        """
        # take the member off the bench and cancel its death watch
        self.idle.discard(crew)
        self.vigils.discard(crew)
        # chain up for the rosters, the channel, and the corpse
        super().bury(crew=crew)
        # and recruit a replacement
        self.recover()
        # all done
        return self

    def dismiss(self, crew):
        """
        Dismiss the {crew} member from the staff
        """
        # chain up to send it home
        super().dismiss(crew=crew)
        # a standing staff replaces members that leave, e.g. ones damaged by their task
        self.recover()
        # all done
        return self

    # implementation details
    def submit(self, channel, crew, **kwds):
        """
        A crew member has reported ready to accept tasks
        """
        # if there is nothing to do at the moment
        if not self.workplan:
            # take the crew member off duty
            self.active.discard(crew)
            # and park it; a future {assemble} will wake it
            self.idle.add(crew)
            # keep an eye on the parked member, so its death gets noticed and its channel
            # stays visible to the event loop; the watch survives wake/repark rounds, since
            # it only clears when its handler fires, so arm at most one per member: a member
            # that was woken but found no work still has its old watch standing
            if crew not in self.vigils:
                # mark it
                self.vigils.add(crew)
                # and arm the watch
                self.dispatcher.whenReadReady(
                    channel=crew.channel, call=functools.partial(self.vigil, crew=crew)
                )
            # and don't reschedule this handler
            return False
        # otherwise, grab the newest task: under load, the most recent requests are the
        # ones their requesters are still looking at
        task, _ = self.workplan.popitem()
        # carefully, since the member may have died while waiting for work
        try:
            # send it off
            crew.execute(team=self, task=task)
        # if its channel is broken
        except OSError:
            # the task was never attempted, so put it back for somebody else
            self.workplan[task] = None
            # and clean up after the member; the replacement will pick the task up
            self.bury(crew=crew)
        # the harvesting of the result decides the fate of this crew member
        return False

    def vigil(self, channel, crew, **kwds):
        """
        The channel of a parked {crew} member has activity

        A parked member has nothing to say, so the only possibility is that it died and its
        end of the channel closed; but if the member has been woken since this watch was set,
        the activity is a task report and belongs to the harvesting handler
        """
        # this watch is spent, whatever happens next; a future park may arm a fresh one
        self.vigils.discard(crew)
        # if the member is no longer parked
        if crew not in self.idle:
            # this watch is stale; drop it without touching the channel
            return False
        # otherwise, the member is gone; clean up after it
        self.bury(crew=crew)
        # and drop the watch
        return False

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # my workplan is an insertion-ordered map that stands in for an ordered set: the
        # keys are the queued tasks, served newest first, and reinsertion renews priority
        self.workplan = {}
        # the bench of parked crew members
        self.idle = set()
        # the members with an armed death watch
        self.vigils = set()
        # the callbacks awaiting task outcomes, keyed by task
        self.pending = {}
        # remember which process manages the staff, so forked members can tell they are not it
        self._manager = os.getpid()
        # the marker that i have been sent home for good
        self._disbanded = False
        # applications may exit by raising from deep inside the event loop, bypassing any
        # orderly shutdown; register the cleanup so crews never outlive me
        atexit.register(self.disband)
        # all done
        return


# end of file
