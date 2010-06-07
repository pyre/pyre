#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Check that the refcount is zero after all nodes have gone out of scope
"""


import pyre.calc


def test():

    n1 = pyre.calc.newNode()
    n2 = pyre.calc.newNode()

    return


# main
if __name__ == "__main__":
    # get the extent manager
    from pyre.patterns.ExtentAware import ExtentAware
    # install it
    pyre.calc._metaclass_Node = ExtentAware
    # run the test
    test()
    # get access to the Node class
    from pyre.calc.Node import Node
    # verify reference counts
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()


# end of file 
