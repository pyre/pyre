#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


"""
Verify that reference nodes correctly reflect the value of their referends
"""


def test():
    import pyre.algebraic

    # make a node and set its value
    v = 80.
    production = pyre.algebraic.var(value=v)
    # make a reference
    clone = production.ref()
    # and a reference to the reference
    clone2 = clone.ref()

    # check
    assert production.value == v
    assert clone.value == v
    assert clone2.value == v
    
    # once more
    v = 100.
    production.value = v
    assert production.value == v
    assert clone.value == v
    assert clone2.value == v

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
