#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a staff executes assigned tasks, delivers their outcomes to callbacks, and keeps
its crew members between assignments
"""

# support
import pyre

# the unit of time
from pyre.units.SI import second


# a task with a recognizable result
class Echo(pyre.nexus.task):
    """
    A task that computes something trivial
    """

    # metamethods
    def __init__(self, tag, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my tag
        self.tag = tag
        # all done
        return

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # hand back a marker
        return f"echo-{self.tag}"


def test():
    # build a staff of one, so member persistence is observable
    staff = pyre.nexus.staff()(name="test.staff.basic")
    staff.size = 1
    # the outcome drop box
    outcomes = []

    # the delivery callback
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

    # assign a first task; let the loop run past the delivery so the member gets parked
    staff.assign(task=Echo(tag=1), callback=record)
    staff.dispatcher.alarm(interval=1 * second, call=expire)
    staff.dispatcher.watch()
    # the outcome arrived
    assert outcomes[0] == ("echo-1", None)
    # and the member survived its assignment, parked on the bench
    assert len(staff.idle) == 1
    # remember who it is
    (veteran,) = staff.idle

    # assign a second task
    staff.assign(task=Echo(tag=2), callback=deliver)
    staff.dispatcher.watch()
    # the outcome arrived
    assert outcomes[1] == ("echo-2", None)
    # served by the same member, not a fresh recruit
    assert set(staff.crews()) == {veteran}

    # send everybody home
    staff.disband()
    # which empties the rosters
    assert list(staff.crews()) == []

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
