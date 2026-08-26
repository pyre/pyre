#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a task assigned to a crew member that died while parked is re-queued and
completed by the replacement
"""

# externals
import os
import signal

# support
import pyre

# the unit of time
from pyre.units.SI import second


# a well behaved task
class Echo(pyre.nexus.task):
    """
    A task with a recognizable result
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # hand back a marker
        return "echo"


def test():
    # build a staff of one
    staff = pyre.nexus.staff()(name="test.staff.misfire")
    staff.size = 1
    # the outcome drop box
    outcomes = []

    # the passive delivery callback
    def record(result, error):
        """
        Record the outcome; leave the loop running so the member gets parked
        """
        # file the report
        outcomes.append((result, error))
        # all done
        return

    # the delivery callback that also stops the loop
    def deliver(result, error):
        """
        Record the outcome and stop the event loop
        """
        # file the report
        outcomes.append((result, error))
        # and wind down
        staff.dispatcher.stop()
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

    # phase 1: get a crew member parked
    staff.assign(task=Echo(), callback=record)
    # let the loop run long enough for the member to finish and get parked
    staff.dispatcher.alarm(interval=1 * second, call=expire)
    staff.dispatcher.watch()
    # the task was delivered and the member is parked
    assert outcomes[0] == ("echo", None)
    assert len(staff.idle) == 1

    # phase 2: kill the parked member and, before the loop can notice, hand it more work
    (crew,) = staff.idle
    # kill it behind the staff's back
    os.kill(crew.pid, signal.SIGKILL)
    # the signal is asynchronous; wait until the member is fully dead, so its end of the
    # channel is certainly closed and the submission is guaranteed to misfire; this also
    # reaps the corpse, which the eventual burial tolerates
    while True:
        # check on it
        corpse, _ = os.waitpid(crew.pid, os.WNOHANG)
        # once it is gone
        if corpse == crew.pid:
            # move on
            break
    # assign a task; this wakes the corpse and schedules it, so the submission will misfire
    staff.assign(task=Echo(), callback=deliver)
    # spin; the submission fails, the task is re-queued, and the replacement delivers it
    staff.dispatcher.watch()

    # the outcome arrived despite the casualty
    assert outcomes[1] == ("echo", None)
    # and the casualty is off the rosters
    assert crew not in set(staff.crews())

    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
