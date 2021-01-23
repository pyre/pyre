#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Verify that the file locator returns the correct location tag
    """
    # access the package
    import pyre.tracking

    # make a locator
    locator = pyre.tracking.file(source="script.py", line=16, column=2)
    # verify the display
    assert str(locator) == "file='script.py', line=16, column=2"

    # all done
    return locator


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
