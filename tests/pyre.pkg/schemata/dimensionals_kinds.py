#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dimensional refuses text that does not evaluate to a quantity or a number, and every
value of any other kind
"""


def test() -> None:
    """
    Coerce things that are not quantities into a dimensional
    """
    # support
    import decimal
    import pyre.schemata

    # make a schema
    schema = pyre.schemata.dimensional()
    # each of these
    for value in (
        "",
        "   ",
        "{}",
        '"abc"',
        "1j",
        "[1, 2]",
        None,
        [1, 2],
        {},
        1j,
        decimal.Decimal("1"),
        object(),
    ):
        # attempt to
        try:
            # coerce it
            schema.coerce(value=value)
            # which should be unreachable
            assert False, value
        # if it is refused, as expected
        except schema.CastingError as error:
            # with the generic complaint
            assert str(error) == f"could not coerce {value!r} into a dimensional quantity", error
    # while the text that spells {None}
    assert schema.coerce(value="none") is None

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
