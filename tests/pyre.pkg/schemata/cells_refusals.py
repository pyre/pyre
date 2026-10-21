#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A cell refuses a name that is not in its table, with the failed lookup as the reason
"""


def test() -> None:
    """
    Give a cell names it does not know, and check the reason each refusal carries
    """
    # support
    import pyre

    # make a cell
    schema = pyre.schemata.cell()

    # names that are not in the table
    for value in ["int7", "real", "const"]:
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
    # do...
    test()


# end of file
