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
    assert (zero == 0).pyre_eval() == True
    assert (one == 1).pyre_eval() == True
    # but also
    assert (zero == one - one).pyre_eval() == True
    assert (zero == one - 1).pyre_eval() == True

    # less-or-equal
    assert (zero <= 0).pyre_eval() == True
    assert (one <= 1).pyre_eval() == True
    # but also
    assert (zero <= one).pyre_eval() == True

    # greater-or-equal
    assert (zero >= 0).pyre_eval() == True
    assert (one >= 1).pyre_eval() == True
    # but also
    assert (one >= zero).pyre_eval() == True

    # less
    assert (zero < one).pyre_eval() == True

    # greater
    assert (one > zero).pyre_eval() == True

    # not-equal
    assert (one != zero).pyre_eval() == True

    return one, zero


# main
if __name__ == "__main__":
    test()


# end of file 
