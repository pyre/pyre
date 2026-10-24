#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that numbers, given directly or as text, are quantities without units, while booleans are not
numbers here
"""


def test() -> None:
    """
    Coerce numbers into a dimensional
    """
    # the schemata
    import pyre.schemata

    # make a schema
    schema = pyre.schemata.dimensional()
    # numbers, and the plain numbers they become
    for value, expected in ((2, 2), (2.5, 2.5), ("2", 2), ("2.5", 2.5), ("0", 0), (-1, -1)):
        # coerce each one
        number = schema.coerce(value=value)
        # it must be the same number, given directly or as text
        assert number == expected and type(number) is type(expected), (value, number)
    # booleans, given directly or as text
    for value in (True, False, "True", "False"):
        # attempt to
        try:
            # coerce each one
            schema.coerce(value=value)
            # which should be unreachable
            assert False, value
        # if it is refused, as expected
        except schema.CastingError:
            # all good
            pass

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
