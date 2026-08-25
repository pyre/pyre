#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a pool can report its current crew members
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
    team = pyre.nexus.pool()(name="test.pool.crews")
    # a fresh team has no members
    assert list(team.crews()) == []

    # make a small workplan
    workplan = {Task() for _ in range(4)}
    # set it up for execution; this recruits crew members
    team.assemble(workplan=workplan)
    # collect the roster
    members = set(team.crews())
    # every recruit is accounted for
    assert members == team.registered | team.active
    # and somebody was actually recruited
    assert members

    # enter the event loop; the team retires when the workplan drains
    team.run()

    # the workplan was fully executed
    assert len(team.workplan) == 0
    # and everybody has retired, so the roster is empty again
    assert list(team.crews()) == []

    # all done
    return team


# main
if __name__ == "__main__":
    test()


# end of file
