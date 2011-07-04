#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise a C expression weaver
"""


def test():
    # get the packages
    import pyre.weaver
    import pyre.algebraic
    # instantiate a weaver
    weaver = pyre.weaver.newWeaver(name="sanity")
    weaver.language = "cxx"
    # access its mill
    mill = weaver.language

    # build a few nodes
    zero = pyre.algebraic.literal(0)
    one = pyre.algebraic.literal(1)
    two = pyre.algebraic.literal(2)

    # check expression generation
    # the trivial cases
    assert mill.expression(zero) == '0'
    assert mill.expression(one) == '1'

    # unary operators
    assert mill.expression(abs(one)) == 'abs(1)'
    assert mill.expression(-one) == '(-1)'

    # binary operators
    assert mill.expression(one + zero) == '(1 + 0)'
    assert mill.expression(one & zero) == '(1 && 0)'
    assert mill.expression(one / zero) == '(1 / 0)'
    assert mill.expression(one == zero) == '(1 == 0)'
    assert mill.expression(one // zero) == '(1 // 0)'
    assert mill.expression(one > zero) == '(1 > 0)'
    assert mill.expression(one >= zero) == '(1 >= 0)'
    assert mill.expression(one < zero) == '(1 < 0)'
    assert mill.expression(one <= zero) == '(1 <= 0)'
    assert mill.expression(one % zero) == '(1 % 0)'
    assert mill.expression(one * zero) == '(1 * 0)'
    assert mill.expression(one != zero) == '(1 != 0)'
    assert mill.expression(one | zero) == '(1 || 0)'
    assert mill.expression(one ** zero) == 'pow(1,0)'
    assert mill.expression(one - zero) == '(1 - 0)'
    
    # return the configured weaver
    return weaver


# main
if __name__ == "__main__":
    test()


# end of file 
