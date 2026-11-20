#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that committing a transaction the server has already abandoned raises, rather than
reporting success while the server rolls the work back
"""


def test():
    """
    Make a statement fail inside a transaction, swallow the error, and commit
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # make a table outside the transaction, so it survives it
    connection.exec("CREATE TEMP TABLE kept (id int)")
    # start a transaction
    transaction = libpq.Transaction(connection)
    # do some work in it
    connection.exec("INSERT INTO kept (id) VALUES (1)")
    # make a statement fail
    try:
        # by dividing by zero
        connection.exec("SELECT 1/0")
    # catch the error
    except exceptions.DataError:
        # and swallow it, as careless code might
        pass
    # the commit cannot succeed, since the server has abandoned the transaction
    try:
        # so try it
        transaction.commit()
    # it must say that the work was not kept
    except exceptions.DatabaseError:
        # which is what we expect
        pass
    # otherwise
    else:
        # complain
        assert False, "the commit of an abandoned transaction reported success"
    # either way, the work is not there
    assert len(connection.exec("SELECT id FROM kept")) == 0
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
