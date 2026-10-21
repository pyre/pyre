#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A boolean refuses a value of a kind it does not support, and text that is not in its table with
the failed lookup as the reason
"""


def test() -> None:
    """
    Give a boolean values it must refuse, and check the reason each refusal carries
    """
    # support
    import pyre

    # make a boolean
    schema = pyre.schemata.bool()

    # values of kinds a boolean does not support
    for value in [1, 0.5, [True], test]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # as a kind it does not support, so there is no reason beyond the complaint
            assert error.error is None, f"{value!r}: {error.error!r}"
        # if it is not refused at all
        else:
            # say so
            assert False, f"accepted {value!r}"

    # text that is not in the table
    for value in ["maybe", "yess", "2"]:
        # carefully
        try:
            # coerce each one
            schema.coerce(value=value)
        # it must be refused
        except schema.CastingError as error:
            # because the lookup failed
            assert isinstance(error.error, KeyError), f"{value!r}: {error.error!r}"
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
