#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the psl selector can raise alarms
"""

# externals
import pyre.ipc
from pyre.units.SI import second
import itertools
from time import time as now


def test():
    # set up a counter
    counter = itertools.count()

    # set up a handler that increments it
    def handler(timestamp):
        # get the next value
        n = next(counter)
        # show me
        # print(f"n: {n}, time: {timestamp}")
        # all done
        return

    # make a selector
    s = pyre.ipc.newPSL(name="pyre.selectors.psl")

    # set up some alarms
    s.alarm(interval=0 * second, call=handler)
    s.alarm(interval=1 * second, call=handler)
    s.alarm(interval=0.5 * second, call=handler)
    s.alarm(interval=0.25 * second, call=handler)
    s.alarm(interval=0.75 * second, call=handler)
    s.alarm(interval=0.3 * second, call=handler)
    s.alarm(interval=0.5 * second, call=handler)
    # record how many alarms were set up
    alarms = len(s._alarms)

    # invoke the selector
    s.watch()
    # verify all alarms had fired when it exited
    assert next(counter) == alarms

    # and return the selector
    return s


# main
if __name__ == "__main__":
    test()


# end of file
