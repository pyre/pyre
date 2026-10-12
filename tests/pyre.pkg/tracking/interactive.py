#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the interactive locator names the user interface the value was set in
"""


def script():
    """
    Make an interactive locator and check how it reads
    """
    # access the package
    import pyre.tracking

    # make a locator for a value set in an editor
    locator = pyre.tracking.interactive(interface="the flow editor")
    # check how it reads
    assert str(locator) == "set interactively in the flow editor"
    # and hand it off
    return locator


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    script()


# end of file
