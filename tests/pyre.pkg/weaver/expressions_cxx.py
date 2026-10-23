#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise a C++ expression weaver
"""


def test():
    # get the package
    import pyre

    # instantiate a weaver
    weaver = pyre.weaver.weaver(name="sanity")
    # that speaks C++
    weaver.language = "cxx"
    # access its mill
    mill = weaver.language

    # build a few nodes
    zero = pyre.calc.var(value=0)
    # and one
    one = pyre.calc.var(value=1)

    # check expression generation
    # the trivial cases
    assert mill.expression(zero) == "0"
    # one renders as itself
    assert mill.expression(one) == "1"

    # arithmetic
    # addition
    assert mill.expression(one + zero) == "(1) + (0)"
    # subtraction
    assert mill.expression(one - zero) == "(1) - (0)"
    # multiplication
    assert mill.expression(one * zero) == "(1) * (0)"
    # division
    assert mill.expression(one / zero) == "(1) / (0)"
    # floor division
    assert mill.expression(one // zero) == "(1) / (0)"
    # remainder
    assert mill.expression(one % zero) == "(1) % (0)"
    # exponentiation
    assert mill.expression(one**zero) == "pow(1,0)"
    # negation
    assert mill.expression(-one) == "-(1)"
    # absolute value
    assert mill.expression(abs(one)) == "abs(1)"

    # comparisons
    assert mill.expression(one == zero) == "(1) == (0)"
    # inequality
    assert mill.expression(one != zero) == "(1) != (0)"
    # less than or equal
    assert mill.expression(one <= zero) == "(1) <= (0)"
    # greater than or equal
    assert mill.expression(one >= zero) == "(1) >= (0)"
    # less than
    assert mill.expression(one < zero) == "(1) < (0)"
    # greater than
    assert mill.expression(one > zero) == "(1) > (0)"

    # boolean
    assert mill.expression(one & zero) == "(1) && (0)"
    # logical or
    assert mill.expression(one | zero) == "(1) || (0)"

    # return the configured weaver
    return weaver


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
