#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A float accepts whatever the {float} constructor accepts, evaluates text first, and refuses
everything else with the constructor's reason, naming the value as it was given
"""


def test() -> None:
    """
    Give a float a value of each kind, and check what becomes of it
    """
    # externals
    import decimal
    import fractions

    # support
    import pyre

    # make a float
    schema = pyre.schemata.float()

    # the values, and what each one must become
    accepted = [
        # a float
        (1.5, 1.5),
        # an infinity
        (float("inf"), float("inf")),
        # numbers of other kinds
        (2, 2.0),
        (True, 1.0),
        (decimal.Decimal("1.5"), 1.5),
        (fractions.Fraction(1, 4), 0.25),
        # text, which is evaluated
        ("1.5", 1.5),
        (" 3/4 ", 0.75),
        ("1e400", float("inf")),
    ]
    # go through them
    for value, expected in accepted:
        # coerce each one
        held = schema.coerce(value=value)
        # it must become the expected value, of the expected type
        assert type(held) is float and held == expected, f"{value!r}: {held!r}"

    # the values the constructor refuses, and the kind of its reason
    refused = [
        # containers
        ([], TypeError),
        ({}, TypeError),
        ({"k": "v"}, TypeError),
        ((1, 2), TypeError),
        # an integer too big to be a float
        (10**400, OverflowError),
        # text whose value the constructor refuses
        ("[]", TypeError),
        ("{}", TypeError),
        ("'abc'", ValueError),
        ("2**10000", OverflowError),
    ]
    # go through them
    for value, reason in refused:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # with the constructor's reason
            assert isinstance(error.error, reason), f"{value!r}: {error.error!r}"
            # naming the value as it was given, rather than what the text evaluated to
            assert error.value is value, f"{value!r}: {error.value!r}"
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
