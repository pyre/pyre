#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that arrays of more than one dimension reach python as nested lists
"""


def test():
    """
    Read a two dimensional array through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for a matrix
    value = connection.exec("SELECT ARRAY[[1, 2], [3, 4]]::int4[] AS matrix")[0]["matrix"]
    # it is a list of its rows
    assert value == [[1, 2], [3, 4]], repr(value)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
