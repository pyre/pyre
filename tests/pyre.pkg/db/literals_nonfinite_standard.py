#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL refuses the values that are not finite, which it has no literals for
"""


def test():
    """
    Render infinities and values that are not numbers, and check that each one is refused
    """
    # support
    import decimal

    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="literals_nonfinite_standard")
    # get its renderer of literals
    literals = mill.literals(mill=mill)

    # the values, and what each one is
    values = [
        # floating point infinities
        (float("inf"), "infinity"),
        (float("-inf"), "infinity"),
        # a floating point value that is not a number
        (float("nan"), "not a number"),
        # a fixed point infinity
        (decimal.Decimal("Infinity"), "infinity"),
        # and a fixed point value that is not a number
        (decimal.Decimal("NaN"), "not a number"),
    ]
    # go through them
    for value, name in values:
        # attempt to
        try:
            # render the value
            literal = literals.value(value=value)
        # which must fail
        except exceptions.NotSupportedError as error:
            # and say why
            assert str(error) == f"standard SQL has no literal for {name}", str(error)
        # if it doesn't
        else:
            # the value was written anyway
            assert False, literal

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
