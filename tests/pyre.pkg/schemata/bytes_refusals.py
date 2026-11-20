#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A string of octets refuses a value of a kind it does not support, and text that is not
hexadecimal digits with the parser's reason
"""


def test() -> None:
    """
    Give a string of octets values it must refuse, and check the reason each refusal carries
    """
    # support
    import pyre

    # make a schema
    schema = pyre.schemata.bytes()

    # a value of a kind a string of octets does not support
    try:
        # coerce it
        schema.coerce(value=5)
    # it must be refused
    except schema.CastingError as error:
        # as a kind it does not support, so there is no reason beyond the complaint
        assert error.error is None, repr(error.error)
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted 5"

    # text that is not hexadecimal digits
    try:
        # coerce it
        schema.coerce(value="xyz")
    # it must be refused
    except schema.CastingError as error:
        # because the digits did not parse
        assert isinstance(error.error, ValueError), repr(error.error)
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted 'xyz'"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
