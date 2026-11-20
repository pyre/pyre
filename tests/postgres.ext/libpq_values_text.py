#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the values of types without a python counterpart reach python as the text the
server wrote
"""


def test():
    """
    Read an {interval} and an {inet} value through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for a value of each
    row = connection.exec(
        "SELECT interval '1 mon 2 days' AS span, inet '192.168.0.1/24' AS address"
    )[0]
    # the interval is its text
    assert row["span"] == "1 mon 2 days", repr(row["span"])
    # and so is the address
    assert row["address"] == "192.168.0.1/24", repr(row["address"])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
