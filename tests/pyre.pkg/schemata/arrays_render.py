#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that arrays render as json with their numbers intact, and as text that reads back as the
same array
"""


def test() -> None:
    """
    Render flat and nested arrays
    """
    # the schemata
    import pyre.schemata

    # make a converter
    schema = pyre.schemata.array()

    # each of these
    for value in ((1.0, 2.0), ((1.0, 2.0), (3.0, 4.0)), ()):
        # reads back from its text
        assert schema.coerce(schema.string(value)) == value, value
    # json keeps the numbers
    assert schema.json(((1.0, 2.0), (3.0, 4.0))) == ((1.0, 2.0), (3.0, 4.0))

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
