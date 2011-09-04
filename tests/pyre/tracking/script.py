#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the script locator returns the correct location tag
"""


def script():
    import pyre.tracking

    locator = pyre.tracking.newScriptLocator(source="script.py", function="script", line=16)
    assert str(locator) == "file='script.py', line=16, function='script'"

    return locator


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    script()


# end of file 
