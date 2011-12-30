#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify nodes with literal values
"""


def test():
    import pyre.calc

    # make a node and set its value
    v = 80.
    production = pyre.calc.var(value=v)
    assert production.value == v
    
    # once more
    v = 100.
    production.value = v
    assert production.value == v

    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.calc" }
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()
    # verify reference counts
    from pyre.calc.Node import Node
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()


# end of file 
