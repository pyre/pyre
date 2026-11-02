#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a PSL selector that goes away without being closed releases the descriptor of its
kernel selector, without help from the cyclic garbage collector
"""

# externals
import gc
import os

# support
import pyre.ipc


def descriptors() -> set[int]:
    """
    Collect the descriptor numbers this process has open
    """
    # the answer
    found = set()
    # go through a range wide enough to hold everything this driver opens
    for candidate in range(256):
        # carefully
        try:
            # ask about this one
            os.fstat(candidate)
        # if it is not open
        except OSError:
            # move on
            continue
        # otherwise, record it
        found.add(candidate)
    # all done
    return found


def test():
    """
    Drop a fresh PSL selector and check that the process is left with the descriptors it had
    """
    # keep the collector out of it, so only the release by the selector itself counts
    gc.disable()
    # take inventory
    before = descriptors()
    # build a selector
    s = pyre.ipc.newPSL()
    # and drop it
    del s
    # the descriptor of the kernel selector must be gone
    assert descriptors() == before
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
