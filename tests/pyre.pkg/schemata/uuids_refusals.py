#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A universally unique identifier refuses a value of a kind it does not support, and text that is
not an identifier with the parser's reason
"""


def test() -> None:
    """
    Give an identifier values it must refuse, and check the reason each refusal carries
    """
    # support
    import pyre

    # make a schema
    schema = pyre.schemata.uuid()

    # a value of a kind an identifier does not support
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

    # text that is not an identifier
    try:
        # coerce it
        schema.coerce(value="a0eebc99")
    # it must be refused
    except schema.CastingError as error:
        # because the identifier did not parse
        assert isinstance(error.error, ValueError), repr(error.error)
    # if it is not refused at all
    else:
        # say so
        assert False, "accepted 'a0eebc99'"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
