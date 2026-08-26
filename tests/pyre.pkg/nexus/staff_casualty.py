#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a staff survives the death of a crew member mid-task: the callback gets the bad
news, and a replacement serves the next assignment
"""

# externals
import os

# support
import pyre


# a task that kills its worker
class Boom(pyre.nexus.task):
    """
    A task whose execution takes down the crew member abruptly, report unsent
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # die without a trace
        os._exit(1)


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
    # build a staff of one, so the casualty is the member that must be replaced
    staff = pyre.nexus.staff()(name="test.staff.casualty")
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

    # assign the lethal task and spin until the outcome is delivered
    staff.assign(task=Boom(), callback=deliver)
    staff.dispatcher.watch()
    # the task produced nothing
    result, error = outcomes[0]
    assert result is None
    # and the failure was reported as a casualty, marking the task as a suspect
    assert isinstance(error, pyre.nexus.exceptions.Casualty)

    # assign a normal task; the replacement crew member should handle it
    staff.assign(task=Echo(), callback=deliver)
    staff.dispatcher.watch()
    # this one succeeded
    assert outcomes[1] == ("echo", None)

    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
