#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a failure of a statement that a server-side function built and ran carries that
statement, and where in it the server gave up
"""


def test():
    """
    Run a statement about a table that does not exist from inside an anonymous PL/pgSQL block
    """
    # access the package
    import pyre.db

    # and the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # carefully
    try:
        # run a block that reads from a table that does not exist
        connection.exec("DO $$ BEGIN EXECUTE 'SELECT 1 FROM nowhere'; END $$")
    # the failure
    except pyre.db.exceptions.DatabaseError as error:
        # carries the statement the block ran
        assert error.internalQuery == "SELECT 1 FROM nowhere", error.internalQuery
        # and points at the name of the missing table in it
        assert error.internalPosition == 15, error.internalPosition
    # a block that succeeds
    else:
        # means the server found a table it should not have
        assert False, "the missing table was not raised"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
