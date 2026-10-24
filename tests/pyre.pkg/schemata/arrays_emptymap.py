#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an empty map is an empty array, as it is an empty list, set or tuple
"""


def test() -> None:
    """
    Convert an empty map, and its text
    """
    # the schemata
    import pyre.schemata

    # make a converter
    schema = pyre.schemata.array()

    # an empty map
    assert schema.coerce({}) == ()
    # and its text
    assert schema.coerce("{}") == ()

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
