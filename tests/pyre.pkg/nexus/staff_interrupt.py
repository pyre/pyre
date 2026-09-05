#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a crew member sets the interrupt key aside, since it is the team's to manage, and
that the team still takes it down when it disbands
"""

# externals
import os
import signal

# support
import pyre

# the unit of time
from pyre.units.SI import second


# a task with a recognizable result
class Echo(pyre.nexus.task):
    """
    A task that reports who ran it
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
        # hand back a marker and the process
        return self.tag, os.getpid()


# the alarm that turns a hang into a failure
def expire(signum, frame):
    """
    Fail loudly rather than wait forever
    """
    # complain
    raise RuntimeError("the team is waiting on a member that will not exit")


def test():
    # build a staff of one, so the same member serves every task
    staff = pyre.nexus.staff()(name="test.staff.interrupt")
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

    # a first task, so the member is known to be up and serving
    staff.assign(task=Echo(tag=1), callback=deliver)
    staff.dispatcher.watch()
    (tag, pid), error = outcomes[0]
    assert (tag, error) == (1, None)
    # the member that served it
    (veteran,) = set(staff.crews())
    assert veteran.pid == pid

    # send it the interrupt key, as a terminal would send it to the whole process group
    os.kill(veteran.pid, signal.SIGINT)
    # it is not for the member: the same one serves the next task as if nothing happened
    staff.assign(task=Echo(tag=2), callback=deliver)
    staff.dispatcher.watch()
    assert outcomes[1] == ((2, pid), None)
    assert set(staff.crews()) == {veteran}

    # disbanding must still take the member down; fail rather than hang if it does not
    signal.signal(signal.SIGALRM, expire)
    signal.alarm(10)
    # send everybody home
    staff.disband()
    # in time
    signal.alarm(0)
    # the rosters are empty
    assert list(staff.crews()) == []
    # and the member is gone; a signal to a reaped process fails
    try:
        # poke it
        os.kill(pid, 0)
    # it must not be there
    except ProcessLookupError:
        # as expected
        pass
    # anything else is a failure
    else:
        # complain
        assert False, "the member survived the disband"

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
