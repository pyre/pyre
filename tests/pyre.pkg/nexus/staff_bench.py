#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the death of a parked crew member is noticed: the watch buries it and a
replacement is recruited
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
    staff = pyre.nexus.staff()(name="test.staff.bench")
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

    # the alarm that winds down the event loop
    def expire(timestamp):
        """
        Stop the event loop
        """
        # ask the dispatcher to stop
        staff.dispatcher.stop()
        # and don't reschedule
        return None

    # assign a task
    staff.assign(task=Echo(), callback=record)
    # let the loop run long enough for the member to finish and get parked
    staff.dispatcher.alarm(interval=1 * second, call=expire)
    staff.dispatcher.watch()
    # the task was delivered and the member is parked
    assert outcomes and outcomes[0] == ("echo", None)
    assert len(staff.idle) == 1

    # get the parked member
    (crew,) = staff.idle
    # and kill it behind the staff's back
    os.kill(crew.pid, signal.SIGKILL)

    # let the loop notice
    staff.dispatcher.alarm(interval=1 * second, call=expire)
    staff.dispatcher.watch()

    # the casualty was buried
    assert crew not in set(staff.crews())
    # and a replacement took its place, so the staff is back at full strength
    assert len(list(staff.crews())) == 1

    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
