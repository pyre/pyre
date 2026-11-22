#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the literals the dialect of postgres writes for the values that are not finite
"""


def test():
    """
    Render infinities and values that are not numbers, and check their literals
    """
    # support
    import decimal

    # access the package
    import pyre.db

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="literals_nonfinite_postgres")
    # get its renderer of literals
    literals = mill.literals(mill=mill)

    # the values, and their literals
    values = [
        # floating point infinities
        (float("inf"), "'Infinity'"),
        (float("-inf"), "'-Infinity'"),
        # a floating point value that is not a number
        (float("nan"), "'NaN'"),
        # fixed point infinities
        (decimal.Decimal("Infinity"), "'Infinity'"),
        (decimal.Decimal("-Infinity"), "'-Infinity'"),
        # and a fixed point value that is not a number
        (decimal.Decimal("NaN"), "'NaN'"),
    ]
    # go through them
    for value, expected in values:
        # render each one
        literal = literals.value(value=value)
        # and check it
        assert literal == expected, (value, literal)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
