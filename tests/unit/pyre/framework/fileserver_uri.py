#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre.framework
    fs = pyre.framework.newFileServer()

    # a simple case
    method, address, fragment = fs.parseURI("pyre.pml")
    assert method == "file"
    assert address == "pyre.pml"
    assert fragment == None

    # another simple case
    method, address, fragment = fs.parseURI("/pyre/system/pyre.pml")
    assert method == "file"
    assert address == "/pyre/system/pyre.pml"
    assert fragment == None

    # the full set
    method, address, fragment = fs.parseURI("file:///pyre.pml#anchor")
    assert method == "file"
    assert address == "/pyre.pml"
    assert fragment == "anchor"

    # a poorly formed one
    try:
        fs.parseURI("file://#anchor")
        assert False
    except fs.BadResourceLocatorError as error:
        assert error.reason == "missing address"

    return fs


# main
if __name__ == "__main__":
    test()


# end of file 
