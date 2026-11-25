#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a postgres server component can be made
"""


def test():
    """
    Make a server component
    """
    # access the package
    import pyre.db

    # build a database component
    db = pyre.db.postgres()
    # it names the default database, which every server has
    assert db.database == "postgres", db.database
    # and holds no session until it attaches
    assert db.connection is None

    # and return it
    return db


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
