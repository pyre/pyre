#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def script():
    """
    Verify that the simple locator returns the correct location tag
    """
    # access the package
    import pyre.tracking

    # make a locator
    locator = pyre.tracking.simple(source="simple")
    # verify the display
    assert str(locator) == "simple"

    # all done
    return locator


# main
if __name__ == "__main__":
    # do...
    script()


# end of file
