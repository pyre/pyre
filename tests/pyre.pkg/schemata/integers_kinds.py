#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
An integer accepts whatever the {int} constructor accepts, evaluates text first, and refuses
everything else with the constructor's reason, naming the value as it was given
"""


def test() -> None:
    """
    Give an integer a value of each kind, and check what becomes of it
    """
    # externals
    import decimal
    import fractions

    # support
    import pyre

    # make an integer
    schema = pyre.schemata.int()

    # the values, and what each one must become
    accepted = [
        # an integer
        (5, 5),
        # a truth value, which the constructor turns into an integer
        (True, 1),
        # numbers of other kinds, which lose their fractional part
        (1.9, 1),
        (decimal.Decimal("1.5"), 1),
        (fractions.Fraction(7, 2), 3),
        # text, which is evaluated
        ("12", 12),
        (" 2*3 ", 6),
        ("2**70", 2**70),
    ]
    # go through them
    for value, expected in accepted:
        # coerce each one
        held = schema.coerce(value=value)
        # it must become the expected value, of the expected type
        assert type(held) is int and held == expected, f"{value!r}: {held!r}"

    # the values the constructor refuses, and the kind of its reason
    refused = [
        # containers
        ([], TypeError),
        ({}, TypeError),
        ({"k": "v"}, TypeError),
        ((1, 2), TypeError),
        # numbers that have no integer value
        (float("inf"), OverflowError),
        (float("nan"), ValueError),
        # text whose value the constructor refuses
        ("[]", TypeError),
        ("{}", TypeError),
        ("'abc'", ValueError),
        ("1e400", OverflowError),
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
