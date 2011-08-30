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

# get the package
import pyre.algebraic
    

def test():

    # declare a couple of nodes
    zero = pyre.algebraic.literal(value=0)
    one = pyre.algebraic.literal(value=1)

    # equality
    assert (zero == 0).eval() == True
    assert (one == 1).eval() == True
    # but also
    assert (zero == one - one).eval() == True
    assert (zero == one - 1).eval() == True

    # less-or-equal
    assert (zero <= 0).eval() == True
    assert (one <= 1).eval() == True
    # but also
    assert (zero <= one).eval() == True

    # greater-or-equal
    assert (zero >= 0).eval() == True
    assert (one >= 1).eval() == True
    # but also
    assert (one >= zero).eval() == True

    # less
    assert (zero < one).eval() == True

    # greater
    assert (one > zero).eval() == True

    # not-equal
    assert (one != zero).eval() == True

    return one, zero


# main
if __name__ == "__main__":
    test()


# end of file 
