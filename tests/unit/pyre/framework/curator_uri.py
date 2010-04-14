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
    curator = pyre.framework.newCurator()

    # a simple case
    method, address, fragment = curator.parseURI("pyre.pml")
    assert method == "file"
    assert address == "pyre.pml"
    assert fragment == None

    # another simple case
    method, address, fragment = curator.parseURI("/pyre/system/pyre.pml")
    assert method == "file"
    assert address == "/pyre/system/pyre.pml"
    assert fragment == None

    # the full set
    method, address, fragment = curator.parseURI("file:///pyre.pml#anchor")
    assert method == "file"
    assert address == "/pyre.pml"
    assert fragment == "anchor"

    # a poorly formed one
    try:
        curator.parseURI("file://#anchor")
        assert False
    except curator.BadResourceLocator as error:
        assert error.reason == "missing address"

    return curator


# main
if __name__ == "__main__":
    test()


# end of file 
