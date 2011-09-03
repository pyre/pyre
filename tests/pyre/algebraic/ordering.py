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
    zero = pyre.algebraic.var(value=0)
    one = pyre.algebraic.var(value=1)

    # equality
    assert (zero == 0).value == True
    assert (one == 1).value == True
    # but also
    assert (zero == one - one).value == True
    assert (zero == one - 1).value == True

    # less-or-equal
    assert (zero <= 0).value == True
    assert (one <= 1).value == True
    # but also
    assert (zero <= one).value == True

    # greater-or-equal
    assert (zero >= 0).value == True
    assert (one >= 1).value == True
    # but also
    assert (one >= zero).value == True

    # less
    assert (zero < one).value == True

    # greater
    assert (one > zero).value == True

    # not-equal
    assert (one != zero).value == True

    return one, zero


# main
if __name__ == "__main__":
    test()


# end of file 
