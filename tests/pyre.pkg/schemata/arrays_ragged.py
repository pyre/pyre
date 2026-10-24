#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an array refuses values whose entries are not all of the same shape
"""


def test() -> None:
    """
    Convert values that are not rectangular
    """
    # the schemata
    import pyre.schemata

    # make a converter
    schema = pyre.schemata.array()

    # each of these
    for value in ([[1, 2], [3]], "[[1, 2], [3]]", [1, [2]], [[1], 2], [[[1]], [2]]):
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
