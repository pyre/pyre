#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that decimal conversions work as expected
"""


def test():
    import decimal
    import pyre.schemata

    # create a descriptor
    descriptor = pyre.schemata.decimal()

    # check
    assert descriptor.coerce("1.20") == decimal.Decimal("1.20")

    # values the decimal constructor rejects, each in its own way
    for value in ["one", [1, 2], {"k": "v"}, object()]:
        # must all
        try:
            # be refused
            descriptor.coerce(value)
            # so getting here is a bug
            assert False, f"{value!r} was converted into a decimal"
        # by the schema
        except descriptor.CastingError as error:
            # with an error that names the value
            assert repr(value) in str(error), str(error)

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
