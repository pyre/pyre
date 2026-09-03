#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a subscriber that fails while taking delivery does not cost the team a member

The delivery of a task's outcome runs code that belongs to whoever asked for the task, inside
the harvest of the member that did the work. If that code raises, the exception reaches the
event loop's caller, as it should; but the member's own fate must be settled regardless, or it
stays counted as busy with nobody listening to it, and the team never hands it work again
"""

# support
import pyre

# the unit of time
from pyre.units.SI import second


# a task that finishes at once
class Quick(pyre.nexus.task):
    """
    A task with nothing to do
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # done already
        return "done"


def test():
    # build a staff of one
    staff = pyre.nexus.staff()(name="test.staff.subscriber")
    staff.size = 1
    # the outcome drop box
    outcomes = []

    # a subscriber that fails while taking delivery, the way one that runs out of file
    # descriptors does
    def failing(result, error):
        """
        Fail on delivery
        """
        # note the delivery
        outcomes.append(("failing", result, error))
        # and fail
        raise OSError(24, "Too many open files")

    # a subscriber that takes delivery
    def record(result, error):
        """
        Record the outcome
        """
        # file the report
        outcomes.append(("record", result, error))
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

    # hand over a task whose subscriber fails
    staff.assign(task=Quick(), callback=failing)
    # run the loop long enough for the member to be recruited, take the task, and report;
    # the failure does not reach us: the dispatcher discards a handler that raises an
    # {OSError}, which is exactly what makes this failure silent in the field
    staff.dispatcher.alarm(interval=1 * second, call=expire)
    staff.dispatcher.watch()
    # the subscriber was served
    assert outcomes == [("failing", "done", None)]

    # the member that did the work is accounted for: it is on the bench, or on its way there
    # with a wake-up pending, and in either case not counted as busy with nobody listening
    (member,) = list(staff.crews())
    assert member not in staff.active or staff.dispatcher._write.get(member.channel.outbound)

    # a second task, with a subscriber that behaves, completes normally
    staff.assign(task=Quick(), callback=record)
    # let the loop run long enough
    staff.dispatcher.alarm(interval=1 * second, call=expire)
    staff.dispatcher.watch()
    # the second outcome arrived
    assert outcomes[-1] == ("record", "done", None)
    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
