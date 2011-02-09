#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that we can traverse the expression tree correctly and completely
"""


def test():

    # access to the basic node
    from pyre.algebraic.Node import Node

    # make a few to use as operands
    n1 = Node()
    n2 = Node()
    n3 = Node()

    # check that they have no dependencies
    assert set(n1.pyre_dependencies) == {n1}
    assert set(n2.pyre_dependencies) == {n2}
    assert set(n3.pyre_dependencies) == {n3}

    # a simple expression
    n = n1 + n2
    assert set(n.pyre_dependencies) == {n1, n2}
    # patch n3 in
    n.pyre_patch(replacements={n1: n3})
    # and check that it happened correctly
    assert set(n.pyre_dependencies) == {n2, n3}

    # a more complicated example
    n = (2*(n1**2 - 2*n1*n2 + n2**2)*n3)
    assert set(n.pyre_dependencies) == {n1, n2, n3}
    # patch n3 in
    n.pyre_patch(replacements={n1: n3})
    # and check that it happened correctly
    assert set(n.pyre_dependencies) == {n2, n3}

    return


# main
if __name__ == "__main__":
    test()


# end of file 
