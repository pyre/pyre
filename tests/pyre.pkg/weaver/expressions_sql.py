#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise an SQL expression weaver
"""


def test():
    """
    Check how the SQL mill renders literals and the operators of expressions
    """
    # get the package
    import pyre

    # instantiate a weaver
    weaver = pyre.weaver.weaver(name="sanity")
    # that speaks SQL
    weaver.language = "sql"
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
    assert mill.expression(one // zero) == "FLOOR((1) / (0))"
    # exponentiation
    assert mill.expression(one**zero) == "POWER(1, 0)"
    # remainder
    assert mill.expression(one % zero) == "MOD(1, 0)"

    # absolute value
    assert mill.expression(abs(one)) == "ABS(1)"
    # negation
    assert mill.expression(-one) == "-(1)"
    # equality
    assert mill.expression(one == zero) == "(1) = (0)"
    # inequality
    assert mill.expression(one != zero) == "(1) <> (0)"
    # less than or equal
    assert mill.expression(one <= zero) == "(1) <= (0)"
    # greater than or equal
    assert mill.expression(one >= zero) == "(1) >= (0)"
    # less than
    assert mill.expression(one < zero) == "(1) < (0)"
    # greater than
    assert mill.expression(one > zero) == "(1) > (0)"

    # logical and
    assert mill.expression(one & zero) == "(1) AND (0)"
    # logical or
    assert mill.expression(one | zero) == "(1) OR (0)"

    # return the configured weaver
    return weaver


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
