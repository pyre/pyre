#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A string of octets accepts octets in any container that holds them, and reads and writes its
text as hexadecimal digits
"""


def test() -> None:
    """
    Coerce octets of each kind, and their text, and write them back
    """
    # support
    import pyre

    # make a schema
    schema = pyre.schemata.bytes()
    # the octets
    octets = b"\x00\xffA"

    # octets pass through
    assert schema.coerce(value=octets) == octets
    # and so do the containers that hold them
    for value in [bytearray(octets), memoryview(octets)]:
        # each of which becomes octets
        assert schema.coerce(value=value) == octets, repr(value)
    # text is hexadecimal digits
    assert schema.coerce(value="00ff41") == octets
    # which is also what my octets write
    assert schema.string(octets) == "00ff41"
    # so they read back
    assert schema.coerce(value=schema.string(octets)) == octets

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
