#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a copy out of the database hands back each row as a line of text
"""


def test():
    """
    Copy two rows out of the database, and check the lines
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # copy two rows out
    lines = list(connection.copyOut("COPY (VALUES (1, 'one'), (2, NULL)) TO STDOUT"))
    # they came out as lines of the text format of a copy
    assert lines == ["1\tone\n", "2\t\\N\n"], lines
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
