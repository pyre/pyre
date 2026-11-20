#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that binary strings reach python as the octets they hold
"""


def test():
    """
    Read a {bytea} value through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for a few octets, a zero among them
    value = connection.exec("SELECT '\\x00ff41'::bytea AS octets")[0]["octets"]
    # they arrive as themselves, not as the text that escapes them
    assert value == b"\x00\xffA", repr(value)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
