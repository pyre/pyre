#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Verify that the file region locator returns the correct location tag
    """
    # access the package
    import pyre.tracking

    # specify a region
    start = pyre.tracking.file(source="script.py", line=16, column=2)
    end = pyre.tracking.file(source="script.py", line=17, column=52)
    # build the locator
    region = pyre.tracking.region(start=start, end=end)
    # verify the display
    assert str(region) == "file='script.py', from (line=16, column=2) to (line=17, column=52)"

    # all done
    return region


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
