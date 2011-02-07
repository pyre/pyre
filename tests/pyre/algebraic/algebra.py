#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise node algebra
"""

# get the base class
from pyre.algebraic.Node import Node
# build a literal
class Literal(Node):

    def eval(self, **kwds):
        return self.value

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

def test():

    # declare a couple of nodes
    n1 = Literal(value=1)
    n2 = Literal(value=2)
    # unary operators
    assert (- n1).eval() == -1
    assert (+ n2).eval() == 2
    assert (abs(n1)).eval() == 1
    # basic arithmetic with two operands
    assert (n1 + n2).eval() == 1 + 2
    assert (n1 - n2).eval() == 1 - 2
    assert (n1 * n2).eval() == 1 * 2
    assert (n1 / n2).eval() == 1 / 2
    assert (n1 // n2).eval() == 1 // 2
    assert (n1 ** n2).eval() == 1 ** 2
    assert (n1 % n2).eval() == 1 % 2

    # basic arithmetic with more than two operands
    assert (n1 + n2 - n1).eval() == 1 + 2 - 1
    assert (n1 * n2 / n1).eval() == 1 * 2 / 1
    assert ((n1 - n2)*n2).eval() == (1 - 2)*2

    # basic arithmetic with constants
    assert (1 + n2).eval() == 1 + 2
    assert (n2 + 1).eval() == 2 + 1
    assert (1 - n2).eval() == 1 - 2
    assert (n2 - 1).eval() == 2 - 1
    assert (2 * n1).eval() == 2 * 1
    assert (n1 * 2).eval() == 1 * 2
    assert (3 / n2).eval() == 3 / 2
    assert (n2 / 3).eval() == 2 / 3
    assert (3 // n2).eval() == 3 // 2
    assert (n2 // 3).eval() == 2 // 3
    assert (3 % n2).eval() == 3 % 2
    assert (n2 % 3).eval() == 2 % 3
    assert (n2 ** 3).eval() == 2**3
    assert (3 ** n2).eval() == 3**2

    # more complicated forms
    assert ((n1**2 + 2*n1*n2 + n2**2)).eval() == ((n1+n2)**2).eval()
    assert ((n1**2 - 2*n1*n2 + n2**2)).eval() == ((n1-n2)**2).eval()
    assert (2*(.5 - n1*n2 + n2**2)*n1).eval() == 2*(.5 - 1*2 + 2**2)*1
    
    return


# main
if __name__ == "__main__":
    test()


# end of file 
