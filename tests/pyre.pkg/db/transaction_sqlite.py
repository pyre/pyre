#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement that begins a transaction in the dialect of sqlite
"""


def test():
    """
    Ask the dialect of sqlite for the statement that begins a transaction
    """
    # access the package
    import pyre.db

    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="transaction_sqlite")
    # build the statement
    statement = tuple(mill.transaction())
    # and check it
    assert statement == ("BEGIN TRANSACTION;",), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
