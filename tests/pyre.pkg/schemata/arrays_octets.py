#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an array of strings of octets takes each string as an entry, as an array of text takes
each string, rather than as a level of octets
"""


def test() -> None:
    """
    Convert arrays of strings of octets, of one and of two levels
    """
    # the schemata
    import pyre.schemata

    # an array of strings of octets
    schema = pyre.schemata.array(schema=pyre.schemata.bytes())
    # holds them as its entries
    assert schema.coerce((b"\x00\xff", b"")) == (b"\x00\xff", b"")

    # and so does one of two levels
    grid = pyre.schemata.array(schema=pyre.schemata.bytes(), rank=2)
    # whose levels are made of them
    assert grid.coerce(((b"a", b"b"), (b"c", b"d"))) == ((b"a", b"b"), (b"c", b"d"))

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
