#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a staff that stands down sends its members home without replacing them, lets a
member that is on a task finish it first, and is back at full strength with its next task
"""

# externals
import os
import time

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


# a task that takes a while
class Nap(pyre.nexus.task):
    """
    A task that is still running when the staff stands down
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # take a while
        time.sleep(0.5)
        # and hand back a marker
        return "nap"


def gone(pid):
    """
    Check whether the process {pid} is gone
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


def test():
    # build a staff of two
    staff = pyre.nexus.staff()(name="test.staff.standdown")
    staff.size = 2
    # the outcome drop box
    outcomes = []

    # the passive delivery callback
    def record(result, error):
        """
        Record the outcome; leave the loop running
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

    # run the event loop for a while
    def run(seconds):
        """
        Let the event loop turn for {seconds}
        """
        # set the alarm
        staff.dispatcher.alarm(interval=seconds * second, call=expire)
        # and turn
        staff.dispatcher.watch()
        # all done
        return

    # give the staff some work, and let the members finish it and get parked
    staff.assign(task=Echo(), callback=record)
    run(seconds=1)
    # the task was delivered and both members are parked
    assert outcomes == [("echo", None)]
    assert len(staff.idle) == 2
    # note who they are
    pids = [crew.pid for crew in staff.idle]

    # stand down
    staff.standDown()
    # the parked members went home
    assert not staff.idle
    assert not list(staff.crews())
    # and their processes are gone
    assert all(gone(pid) for pid in pids)
    # nobody was recruited in their place, even after the loop turns
    run(seconds=1)
    assert not list(staff.crews())

    # back to work
    staff.assign(task=Nap(), callback=record)
    # which brings the staff back to full strength
    assert len(list(staff.crews())) == 2
    # let the members check in and start on the task
    run(seconds=0.2)
    # stand down while one of them is still napping
    staff.standDown()
    # the one that is on a task finishes it, and then everybody goes home
    run(seconds=1.5)
    assert outcomes[-1] == ("nap", None)
    assert not list(staff.crews())

    # and the staff can still be sent home for good
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
