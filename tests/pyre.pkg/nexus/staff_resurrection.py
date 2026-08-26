#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a disbanded staff stays disbanded: recoveries do not resurrect it, and new work
is refused immediately
"""

# support
import pyre


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
    staff = pyre.nexus.staff()(name="test.staff.resurrection")
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

    # assign a task and spin until it is delivered
    staff.assign(task=Echo(), callback=deliver)
    staff.dispatcher.watch()
    # the task succeeded
    assert outcomes[0] == ("echo", None)

    # send everybody home
    staff.disband()
    # nobody is left
    assert list(staff.crews()) == []

    # a recovery arriving after disband must not resurrect the staff
    staff.recover()
    # still nobody
    assert list(staff.crews()) == []

    # and new work is refused on the spot
    staff.assign(task=Echo(), callback=deliver)
    # with the bad news delivered synchronously
    result, error = outcomes[1]
    assert result is None
    assert error is not None
    # and no crews were recruited for it
    assert list(staff.crews()) == []

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
