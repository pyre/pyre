#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a staff serves its workplan newest first: under load, the most recent requests
are the ones their requesters are still looking at
"""

# support
import pyre


# a task with a recognizable result
class Echo(pyre.nexus.task):
    """
    A task that reports its tag
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
        # hand back my tag
        return self.tag


def test():
    # build a staff of one, so the queue drains strictly sequentially
    staff = pyre.nexus.staff()(name="test.staff.priority")
    staff.size = 1
    # the record of deliveries, in order
    served = []

    # the delivery callback
    def deliver(result, error):
        """
        Record the outcome, and stop once everybody has been served
        """
        # every task succeeds
        assert error is None
        # record the tag
        served.append(result)
        # if all four are in
        if len(served) == 4:
            # wind down
            staff.dispatcher.stop()
        # all done
        return

    # queue four tasks before the event loop runs, so they pile up
    for tag in (1, 2, 3, 4):
        # each with the shared callback
        staff.assign(task=Echo(tag=tag), callback=deliver)
    # spin until all four are delivered
    staff.dispatcher.watch()

    # the queue drained newest first
    assert served == [4, 3, 2, 1], f"out of order: {served}"

    # send everybody home
    staff.disband()
    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
