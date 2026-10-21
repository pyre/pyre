#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A fraction refuses malformed text, values of the wrong type, and values with no ratio, with
the reason the constructor gave
"""


def test() -> None:
    """
    Give a fraction values it must refuse, and check the reason each refusal carries
    """
    # support
    import pyre

    # make a fraction
    schema = pyre.schemata.fraction()

    # the values, and the kind of reason each one is refused for
    cases = [
        # malformed text
        ("one half", ValueError),
        # a value of the wrong type
        ([1, 2], TypeError),
        # a zero denominator
        ("1/0", ZeroDivisionError),
        # an infinity
        (float("inf"), OverflowError),
        # not a number
        (float("nan"), ValueError),
    ]
    # go through them
    for value, reason in cases:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # for the expected reason
            assert isinstance(error.error, reason), f"{value!r}: {error.error!r}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
