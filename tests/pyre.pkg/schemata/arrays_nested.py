#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an array without a declared rank or shape takes values of any depth, as nested tuples
"""


def test() -> None:
    """
    Convert nested sequences, and their text
    """
    # the schemata
    import pyre.schemata

    # make a converter
    schema = pyre.schemata.array()

    # a flat sequence
    assert schema.coerce("[1, 2]") == (1.0, 2.0)
    # a matrix
    assert schema.coerce([[1, 2], [3, 4]]) == ((1.0, 2.0), (3.0, 4.0))
    # its text
    assert schema.coerce("[[1, 2], [3, 4]]") == ((1.0, 2.0), (3.0, 4.0))
    # a deeper one
    assert schema.coerce(((1,),)) == ((1.0,),)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
