#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A complex number accepts whatever the {complex} constructor accepts, and sequences of its
parts; it evaluates text first, refuses maps and empty sequences as kinds it does not support,
and everything else with the constructor's reason, naming the value as it was given
"""


def test() -> None:
    """
    Give a complex number a value of each kind, and check what becomes of it
    """
    # externals
    import decimal
    import fractions

    # support
    import pyre

    # make a complex number
    schema = pyre.schemata.complex()

    # the values, and what each one must become
    accepted = [
        # a complex number
        (1 + 2j, 1 + 2j),
        # numbers of other kinds
        (2, 2 + 0j),
        (1.5, 1.5 + 0j),
        (decimal.Decimal("1.5"), 1.5 + 0j),
        (fractions.Fraction(1, 4), 0.25 + 0j),
        # sequences of parts
        ((1, 2), 1 + 2j),
        ([1, 2], 1 + 2j),
        ([3], 3 + 0j),
        # text, which is evaluated
        ("1+2j", 1 + 2j),
        ("(1, 2)", 1 + 2j),
        # including text that evaluates to text the constructor understands
        ("'1+2j'", 1 + 2j),
    ]
    # go through them
    for value, expected in accepted:
        # coerce each one
        held = schema.coerce(value=value)
        # it must become the expected value, of the expected type
        assert type(held) is complex and held == expected, f"{value!r}: {held!r}"

    # kinds a complex number does not support, as given or as text evaluates to them
    for value in [{}, {"k": "v"}, [], (), "{}", "[]"]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # as a kind it does not support, so there is no reason beyond the complaint
            assert error.error is None, f"{value!r}: {error.error!r}"
            # naming the value as it was given
            assert error.value is value, f"{value!r}: {error.value!r}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # the values the constructor refuses, and the kind of its reason
    refused = [
        # too many parts
        ((1, 2, 3), TypeError),
        # parts that are not numbers
        ([[1], 2], TypeError),
        # an integer too big to be a part
        (10**400, OverflowError),
        # text whose value the constructor refuses
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
