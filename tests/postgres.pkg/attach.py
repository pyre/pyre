#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a postgres server component attaches to its default database
"""


def test():
    """
    Make a server component and attach it
    """

    # access the postgres package
    import pyre.db

    # build a database component
    db = pyre.db.postgres()
    # connect to the default database
    db.attach()

    # the session is up
    assert db.connection.ok
    # on the default database
    ((name,),) = db.execute("SELECT current_database()")
    # which is the one the component names
    assert name == "postgres", name

    # and return the component
    return db


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
