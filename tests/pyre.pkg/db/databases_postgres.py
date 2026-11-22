#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statements the dialect of postgres builds to create and drop a database
"""


def test():
    """
    Ask the dialect of postgres for the statements that create and drop a database
    """
    # access the package
    import pyre.db

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.dialects.postgres(name="databases_postgres")

    # build the statement that creates a database
    statement = tuple(mill.createDatabase(name="inventory"))
    # and check it
    assert statement == ("CREATE DATABASE inventory;",), statement

    # build the statement that drops it
    statement = tuple(mill.dropDatabase(name="inventory"))
    # and check it
    assert statement == ("DROP DATABASE inventory;",), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
