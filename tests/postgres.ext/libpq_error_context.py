#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a failure inside a server-side function carries the server's account of where it
happened
"""


def test():
    """
    Divide by zero inside an anonymous PL/pgSQL block, and look for the block in the context
    """
    # access the package
    import pyre.db

    # and the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # carefully
    try:
        # run a block that divides by zero
        connection.exec("DO $$ BEGIN PERFORM 1/0; END $$")
    # the failure
    except pyre.db.exceptions.DatabaseError as error:
        # names the function the statement ran in
        assert "PL/pgSQL function" in error.context, error.context
        # and the statement inside it that failed
        assert 'SQL statement "SELECT 1/0"' in error.context, error.context
    # a block that succeeds
    else:
        # means the server never saw the division
        assert False, "the division by zero was not raised"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
