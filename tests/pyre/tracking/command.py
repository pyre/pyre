#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
    script()


# end of file 
