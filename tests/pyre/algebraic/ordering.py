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


def test():
    # get the package
    import pyre.algebraic

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
    assert (zero != one).value == True
    assert (zero != 1).value == True
    assert (zero != 0).value == False
    assert (one != zero).value == True
    assert (one != 0).value == True
    assert (one != 1).value == False

    return one, zero


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
