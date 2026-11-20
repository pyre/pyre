#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that booleans reach python as booleans, so that a false value is false in a test
"""


def test():
    """
    Read a true and a false value through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for one of each
    row = connection.exec("SELECT true AS yes, false AS no")[0]
    # the true one is {True}
    assert row["yes"] is True, repr(row["yes"])
    # and the false one is {False}, and hence false in a test
    assert row["no"] is False, repr(row["no"])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
