#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# support
import pyre

# the unit of time
from pyre.units.SI import second


# a task that never finishes
class Forever(pyre.nexus.task):
    """
    A task that outlives any patience
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # externals
        import time

        # take far longer than the team is willing to wait
        time.sleep(30)
        # and never get here
        return "done"


def test():
    """
    Verify that a task which outlives the team's patience is answered for

    A team whose members are separate processes is exposed to a worker that accepts a task and never
    reports: it may be wedged, it may be waiting on something that will never arrive, or it may
    simply be slower than anybody is willing to wait for. Without a limit the requester holds a
    promise that is never kept, and every task queued behind that member waits with it. So a team
    may declare how long it is prepared to wait; when the deadline passes the task is abandoned with
    a recoverable error, the member is buried on the assumption that a worker nobody can trust is
    worse than none, and a replacement takes its place
    """
    # build a staff of one that will not wait long
    staff = pyre.nexus.staff()(name="test.staff.patience")
    staff.size = 1
    staff.patience = 1 * second
    # the outcome drop box
    outcomes = []

    # the passive delivery callback
    def record(result, error):
        """
        Record the outcome
        """
        # file the report
        outcomes.append((result, error))
        # all done
        return

    # the alarm that winds down the event loop
    def expire(timestamp):
        """
        Stop the event loop
        """
        # ask the dispatcher to stop
        staff.dispatcher.stop()
        # and don't reschedule
        return None

    # hand over a task nobody will ever hear the end of
    staff.assign(task=Forever(), callback=record)
    # give the member long enough to be recruited and take it
    staff.dispatcher.alarm(interval=1 * second / 2, call=expire)
    # by running the loop until then
    staff.dispatcher.watch()
    # then get the member
    (member,) = staff.active
    # and remember which process it is, so we can ask afterwards whether anybody cleaned up
    overrun = member.pid
    # now let the loop run well past the deadline
    staff.dispatcher.alarm(interval=4 * second, call=expire)
    # and run it
    staff.dispatcher.watch()

    # the requester was told, rather than left waiting
    assert len(outcomes) == 1
    # with nothing to show for it
    result, error = outcomes[0]
    # no result
    assert result is None
    # and a reason it can act on: this one is worth asking about again
    assert isinstance(error, staff.RecoverableError)
    # because the task took too long
    assert "took too long" in error.description

    # the member that swallowed the task is gone from the rosters
    assert len(staff.active) == 0
    # and gone from the process table too: a deadline that left the worker running would
    # trade a stalled queue for a process nobody owns, still burning a core on work whose
    # answer has already been given up on
    try:
        # probe it
        os.kill(overrun, 0)
    # which is what a reaped process does
    except (OSError, ProcessLookupError):
        # so there is nothing left of it
        pass
    # otherwise it is still out there
    else:
        # and that is a leak
        assert False, "the overrun worker survived its deadline"
    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
