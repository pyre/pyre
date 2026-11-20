#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that json documents reach python as the values they describe
"""


def test():
    """
    Read a {json} and a {jsonb} value through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for one of each
    row = connection.exec(
        """SELECT '{"a": [1, 2.5, null, true]}'::json AS plain,"""
        """ '{"a": [1, 2.5, null, true]}'::jsonb AS binary"""
    )[0]
    # both describe the same value
    expected = {"a": [1, 2.5, None, True]}
    # the plain document arrives as it
    assert row["plain"] == expected, repr(row["plain"])
    # and so does the binary one
    assert row["binary"] == expected, repr(row["binary"])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
