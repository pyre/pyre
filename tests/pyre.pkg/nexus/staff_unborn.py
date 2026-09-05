#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a crew member dismissed before it has checked in still exits, so the team is not
left waiting for it forever
"""

# externals
import signal

# support
import pyre


# a task nobody will run
class Idle(pyre.nexus.task):
    """
    A task that is never executed
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # nothing
        return None


# the alarm that turns a hang into a failure
def expire(signum, frame):
    """
    Fail loudly rather than wait forever
    """
    # complain
    raise RuntimeError("the team is waiting on a member that will not exit")


def test():
    # build a staff of one
    staff = pyre.nexus.staff()(name="test.staff.unborn")
    staff.size = 1
    # assigning a task recruits the member; its check-in is on the wire but nobody has run the
    # loop yet, so the team has not heard it
    staff.assign(task=Idle(), callback=lambda result, error: None)
    # a member has been deployed and is still registering
    assert len(staff.registered) == 1

    # disbanding must not wait forever on the member, whose check-in will fail because the
    # team lets go of its end of the crew channel; the member has to notice and exit
    signal.signal(signal.SIGALRM, expire)
    signal.alarm(10)
    # send everybody home
    staff.disband()
    # in time
    signal.alarm(0)
    # and the rosters are empty
    assert list(staff.crews()) == []

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
