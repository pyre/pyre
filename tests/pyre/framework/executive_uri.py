#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise URI parsing by the executive
"""


def test():
    import pyre.framework
    executive = pyre.framework.executive()

    # a simple case
    method, address, fragment = executive.parseURI("pyre.pml")
    assert method == "file"
    assert address == "pyre.pml"
    assert fragment == None

    # another simple case
    method, address, fragment = executive.parseURI("/pyre/system/pyre.pml")
    assert method == "file"
    assert address == "/pyre/system/pyre.pml"
    assert fragment == None

    # the full set
    method, address, fragment = executive.parseURI("file:///pyre.pml#anchor")
    assert method == "file"
    assert address == "/pyre.pml"
    assert fragment == "anchor"

    # a poorly formed one
    try:
        executive.parseURI("file://#anchor")
        assert False
    except executive.BadResourceLocatorError as error:
        assert error.reason == "missing address"

    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
