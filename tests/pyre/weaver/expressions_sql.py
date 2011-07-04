#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise a python expression weaver
"""


def test():
    # get the packages
    import pyre.weaver
    import pyre.algebraic
    # instantiate a weaver
    weaver = pyre.weaver.newWeaver(name="sanity")
    weaver.language = "sql"
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
    assert mill.expression(abs(one)) == '@(1)'
    assert mill.expression(-one) == '(-1)'

    # binary operators
    assert mill.expression(one + one) == '(1 + 1)'
    assert mill.expression(one & one) == '(1 AND 1)'
    assert mill.expression(one / one) == '(1 / 1)'
    assert mill.expression(one == one) == '(1 = 1)'
    assert mill.expression(one > one) == '(1 > 1)'
    assert mill.expression(one >= one) == '(1 >= 1)'
    assert mill.expression(one < one) == '(1 < 1)'
    assert mill.expression(one <= one) == '(1 <= 1)'
    assert mill.expression(one % one) == '(1 % 1)'
    assert mill.expression(one * one) == '(1 * 1)'
    assert mill.expression(one != one) == '(1 <> 1)'
    assert mill.expression(one | one) == '(1 OR 1)'
    assert mill.expression(one ** one) == '(1 ^ 1)'
    assert mill.expression(one - one) == '(1 - 1)'
    
    # return the configured weaver
    return weaver


# main
if __name__ == "__main__":
    test()


# end of file 
