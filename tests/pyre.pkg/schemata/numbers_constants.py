#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The text of a numeric setting may use the constants of {math}, by name and by greek letter
"""


def test() -> None:
    """
    Evaluate the constants as floats
    """
    # externals
    import math

    # support
    import pyre

    # make a float
    schema = pyre.schemata.float()

    # the text, and the constant it must evaluate to
    constants = [
        # by name
        ("pi", math.pi),
        ("tau", math.tau),
        ("e", math.e),
        # by greek letter
        ("π", math.pi),
        ("τ", math.tau),
        # in an expression
        ("τ/2", math.pi),
    ]
    # go through them
    for text, expected in constants:
        # coerce each one
        held = schema.coerce(value=text)
        # it must be the constant
        assert held == expected, f"{text!r}: {held!r}"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
