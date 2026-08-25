#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a pool can be configured to manage its crew over the socket transport
"""

# support
import pyre


# my task
class Task(pyre.nexus.task):
    """
    A trivial task with a recognizable result
    """

    # interface
    def execute(self):
        """
        The body of the task
        """
        # hand back a marker
        return "done"


def test():
    # get the pool component from its foundry and build a team
    team = pyre.nexus.pool()(name="test.pool.sockets")
    # ask its recruiter to manage the crew over the socket transport
    team.recruiter.channels = "socket"
    # verify the selection stuck
    assert team.recruiter.channels.pyre_family() == "pyre.ipc.transports.socket"

    # make a small workplan
    workplan = {Task() for _ in range(4)}
    # set it up for execution
    team.assemble(workplan=workplan)
    # and enter the event loop; the team retires when the workplan drains
    team.run()

    # the workplan was fully executed
    assert len(team.workplan) == 0
    # no crew members are still on the clock
    assert len(team.active) == 0

    # all done
    return team


# main
if __name__ == "__main__":
    test()


# end of file
