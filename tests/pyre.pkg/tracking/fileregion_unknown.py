#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the region locator leaves out the parts of its ends that are unknown
"""


def test() -> None:
    """
    Render a region whose start has no column and whose end has no line
    """
    # get the package
    import pyre.tracking

    # the start of the region, without a column
    start = pyre.tracking.file(source="script.py", line=16)
    # and its end, without a line
    end = pyre.tracking.file(source="script.py", column=52)
    # make the region
    region = pyre.tracking.region(start=start, end=end)
    # check that each end shows only what is known about it
    assert str(region) == "file='script.py', from (line=16) to (column=52)"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
