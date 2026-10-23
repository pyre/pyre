#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise node algebra
"""


def test():
    # access the package
    import pyre.calc

    # declare a couple of nodes
    n1 = pyre.calc.var(value=1)
    # and another one
    n2 = pyre.calc.var(value=2)
    # unary operators
    assert (-n1).value == -1
    # unary plus
    assert (+n2).value == 2
    # absolute value
    assert (abs(n1)).value == 1
    # basic arithmetic with two operands
    assert (n1 + n2).value == 1 + 2
    # subtraction
    assert (n1 - n2).value == 1 - 2
    # multiplication
    assert (n1 * n2).value == 1 * 2
    # division
    assert (n1 / n2).value == 1 / 2
    # assert (n1 // n2).value == 1 // 2 # NYI
    # basic arithmetic with more than two operands
    assert (n1 + n2 - n1).value == 1 + 2 - 1
    # products and quotients
    assert (n1 * n2 / n1).value == 1 * 2 / 1
    # grouping
    assert ((n1 - n2) * n2).value == (1 - 2) * 2
    # basic arithmetic with numbers
    assert (1 + n2).value == 1 + 2
    # addition with the number on the right
    assert (n2 + 1).value == 2 + 1
    # subtraction from a number
    assert (1 - n2).value == 1 - 2
    # subtraction of a number
    assert (n2 - 1).value == 2 - 1
    # multiplication with the number on the left
    assert (2 * n1).value == 2 * 1
    # multiplication with the number on the right
    assert (n1 * 2).value == 1 * 2
    # a number divided by a node
    assert (3 / n2).value == 3 / 2
    # a node divided by a number
    assert (n2 / 3).value == 2 / 3
    # a node raised to a numeric power
    assert (n2**3).value == 2**3
    # a number raised to the power of a node
    assert (3**n2).value == 3**2

    # more complicated forms
    assert ((n1**2 + 2 * n1 * n2 + n2**2)).value == ((n1 + n2) ** 2).value
    # the square of a difference
    assert ((n1**2 - 2 * n1 * n2 + n2**2)).value == ((n1 - n2) ** 2).value
    # a mix of nodes and numbers in nested groups
    assert (2 * (0.5 - n1 * n2 + n2**2) * n1).value == 2 * (0.5 - 1 * 2 + 2**2) * 1

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
