#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the rows sent through a copy land in the table, each python value as its column reads
it, with {None} as {NULL}
"""


def test():
    """
    Copy two rows of several types into a table, and read them back
    """
    # support
    import datetime

    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # make a table of our own, which goes away with the session
    connection.exec("CREATE TEMPORARY TABLE pyre_copy (id integer, name text, day date)")

    # copy two rows into it
    with connection.copyIn("COPY pyre_copy (id, name, day) FROM STDIN") as copy:
        # one with every value
        copy.row(1, "one\ttab", datetime.date(2026, 11, 24))
        # and one with a missing value
        copy.row(2, None, datetime.date(2026, 11, 25))

    # read them back
    rows = list(connection.exec("SELECT id, name, day FROM pyre_copy ORDER BY id"))
    # they are there, with their values
    assert [tuple(row) for row in rows] == [
        (1, "one\ttab", datetime.date(2026, 11, 24)),
        (2, None, datetime.date(2026, 11, 25)),
    ], rows
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
