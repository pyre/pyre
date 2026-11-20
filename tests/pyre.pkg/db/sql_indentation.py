#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a statement abandoned halfway, or one with nothing in it, leaves the next statement
at the margin
"""


def test():
    """
    Abandon a statement after its first line, generate an empty insert, then generate another
    """
    # access the package
    import pyre.db

    # a table with a docstring and a few fields, so its statement indents its body
    class Plain(pyre.db.table, id="plain"):
        """
        A table with nothing special about it
        """

        # the first field
        first = pyre.db.int()
        # the second
        second = pyre.db.int()
        # and the third
        third = pyre.db.int()

    # what the statement looks like when nothing has gone wrong before it
    expected = tuple(pyre.db.server(name="fresh").sql.createTable(Plain))

    # get another server
    server = pyre.db.server(name="used")
    # start a statement
    lines = server.sql.createTable(Plain)
    # read a few lines, into its body
    for _ in range(4):
        # one at a time
        next(lines)
    # and abandon the rest
    # then ask for an insert with nothing to insert
    tuple(server.sql.insertRecords())
    # the next statement is laid out as if nothing had happened
    statement = tuple(server.sql.createTable(Plain))
    # so check
    assert statement == expected, "\n".join(statement)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
