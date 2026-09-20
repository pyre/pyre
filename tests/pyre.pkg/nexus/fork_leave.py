#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a crew member ends its process without running the exit handlers it inherited from
the team, after it gets the chance to put its own affairs in order

A crew member is a fork of the team's process. The exit handlers it would run belong to the
team: they were registered in a process with state the member does not share, and one that
waits for a thread that did not survive the fork would keep the member from ever leaving
"""

# externals
import atexit
import os

# support
import pyre
from pyre.units.SI import second


# the files the two sides leave behind
def inherited(pid):
    # the mark of an inherited exit handler that ran in process {pid}
    return f"fork_leave.handler.{pid}"


def retired(pid):
    # the mark of a crew member that retired in process {pid}
    return f"fork_leave.retired.{pid}"


# a crew member that leaves a mark when it retires
class Retiree(pyre.nexus.crew):
    """
    A crew member that records its retirement
    """

    # interface
    def retire(self):
        # leave a mark, named after the process this runs in
        open(retired(pid=os.getpid()), "w").close()
        # and chain up
        return super().retire()


# a staff of such members
class Office(pyre.nexus.staff()):
    """
    A staff whose members record their retirement
    """

    # my crew members
    crew = Retiree


# a task that reports who carried it out
class Who(pyre.nexus.task):
    """
    A task that hands back the process id of whoever executes it
    """

    # interface
    def execute(self, **kwds):
        # easy enough
        return os.getpid()


def test():
    # the process that registers the handler
    me = os.getpid()

    # the exit handler: it leaves a mark named after the process that runs it, unless that is
    # the process that registered it, which has every right to run it
    def handler():
        # if this is somebody else
        if os.getpid() != me:
            # leave the mark
            open(inherited(pid=os.getpid()), "w").close()
        # all done
        return

    # register it before anybody is forked, so that every crew member inherits it
    atexit.register(handler)

    # build a staff of one
    staff = Office(name="test.fork.leave")
    staff.size = 1
    # the outcome drop box
    outcomes = []

    # wind down once the member is parked: a member that is still on the active roster when
    # the staff disbands is terminated on the spot, since its work is moot, and never gets to
    # leave on its own, which is the very thing under test
    def settle(timestamp):
        # if the member is not parked yet
        if not staff.idle:
            # check back shortly
            return 0.01 * second
        # otherwise, wind down
        staff.dispatcher.stop()
        # and don't reschedule
        return None

    # the delivery callback
    def deliver(result, error):
        # file the report
        outcomes.append((result, error))
        # and start checking whether the member has been parked
        staff.dispatcher.alarm(interval=0.01 * second, call=settle)
        # all done
        return

    # assign the task and spin until the outcome is delivered
    staff.assign(task=Who(), callback=deliver)
    staff.dispatcher.watch()
    # the outcome arrived, from somebody else
    member, error = outcomes[0]
    assert error is None
    assert member != os.getpid()

    # send everybody home; this harvests the member, so it is gone when the call returns
    staff.disband()

    # the member got to put its affairs in order
    assert os.path.exists(retired(pid=member))
    # and left without running the exit handler it inherited
    assert not os.path.exists(inherited(pid=member))

    # clean up after the member
    os.remove(retired(pid=member))
    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
