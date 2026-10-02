#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that {here} records the location of its caller, or of a caller further up when asked,
without reading any source files
"""

# externals
import sys


def caller():
    """
    Ask for a locator that records this function, and one that records my caller
    """
    # get the package
    import pyre.tracking

    # the line number of the first request
    line = sys._getframe().f_lineno + 2
    # a locator for this function
    mine = pyre.tracking.here()
    # and one for my caller
    theirs = pyre.tracking.here(level=1)
    # hand them off, along with the line of the first
    return mine, theirs, line


def test():
    # get the package now, so its import is not mistaken for reading source files
    import pyre.tracking

    # the files the test opens
    opened = []

    # record the files that get opened
    def hook(event, args):
        """
        Watch for file opens
        """
        # if a file is being opened
        if event == "open":
            # record it
            opened.append(args[0])
        # all done
        return

    # watch
    sys.addaudithook(hook)
    # the line of the call below
    line = sys._getframe().f_lineno + 2
    # get the locators
    mine, theirs, callerLine = caller()
    # the first one records the function that asked for it
    assert mine.source == __file__
    assert mine.line == callerLine
    assert mine.function == "caller"
    # the second one records its caller
    assert theirs.source == __file__
    assert theirs.line == line
    assert theirs.function == "test"
    # and nothing was read to build them
    assert not opened, opened
    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
