#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an array is converted whole or not at all: an entry that fails refuses the value, and
the complaint names the entry rather than the shape it leaves behind
"""


def test() -> None:
    """
    Convert values with entries that are not numbers
    """
    # the schemata
    import pyre.schemata

    # make a converter
    schema = pyre.schemata.array()

    # attempt to
    try:
        # convert a matrix with a bad entry
        schema.coerce([[1, 2], [3, "x"]])
        # which should be unreachable
        assert False, "unreachable"
    # if it is refused, as expected
    except schema.CastingError as error:
        # check that the complaint names the entry
        assert "'x'" in str(error), str(error)

    # each of these
    for value in ([1, "x", 3], "[1, 'x']"):
        # attempt to
        try:
            # convert it
            schema.coerce(value)
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
