#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a name cannot carry a statement of its own into the one that names it
"""


def test():
    """
    Create a database whose name holds a second statement, and check it stays a name
    """
    # access the package
    import pyre.db

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="identifiers")
    # build the statement that creates a database with a hostile name
    statement = tuple(mill.createDatabase(name="a; DROP TABLE t"))
    # and check the name stays a name
    assert statement == ('CREATE DATABASE "a; DROP TABLE t";',), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
