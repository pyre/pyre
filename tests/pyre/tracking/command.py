#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that the command locator returns the correct location tag
"""


def script():
    import pyre.tracking

    locator = pyre.tracking.newCommandLocator(arg=4)

    assert str(locator) == "command line, arg 4"

    return locator


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    script()


# end of file 
