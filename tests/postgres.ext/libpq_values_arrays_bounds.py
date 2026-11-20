#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an array that does not start at one reaches python as a plain list
"""


def test():
    """
    Read an array whose first entry is at zero through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for an array with explicit bounds
    value = connection.exec("SELECT '[0:2]={7,8,9}'::int4[] AS shifted")[0]["shifted"]
    # the bounds are gone, and the entries are all there
    assert value == [7, 8, 9], repr(value)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
