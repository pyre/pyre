#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2025 all rights reserved
#


"""
Instantiate the postgres component
"""


def test():
    # access the package
    import pyre.db

    # build a database component
    db = pyre.db.postgres()
    # verify it is going to attach to the default database that is guaranteed to exist
    assert db.database == "postgres"
    # attach
    db.attach()

    # create the pyre database
    db.dropDatabase(name="pyre")

    # and return the component
    return db


# main
if __name__ == "__main__":
    test()


# end of file
