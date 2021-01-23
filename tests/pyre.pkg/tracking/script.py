#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def script():
    """
    Verify that the script locator returns the correct location tag
    """
    # get the package
    import pyre.tracking

    # make a locator
    locator = pyre.tracking.script(source=__file__, function="script", line=16)
    # verify the display
    assert str(locator) == f"file='{__file__}', line=16, function='script'"

    # all done
    return locator


# main
if __name__ == "__main__":
    # do...
    script()


# end of file
