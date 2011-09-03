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
    import pyre.algebraic

    # make a few to use as operands
    n1 = pyre.algebraic.var()
    n2 = pyre.algebraic.var()

    # check that they have no dependencies
    assert set(n1.variables) == {n1}
    assert set(n2.variables) == {n2}

    # an expression involving a unary operator
    n = -n1
    assert set(n.variables) == {n1}
    
    # an expression involving a pseudo-unary operator
    n = 2*n1
    assert set(n.variables) == {n1}
    
    # an expression involving a binary operator
    n = n1 + n2
    assert set(n.variables) == {n1, n2}
    
    # a more complicated example
    assert set((2*(.5 - n1*n2 + n2**2)*n1).variables) == {n1, n2}

    return


# main
if __name__ == "__main__":
    test()


# end of file 
