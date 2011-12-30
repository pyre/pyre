#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Instantiate the postgres component
"""


def test():
    # access the package
    import postgres

    # build a database component
    db = postgres.server()
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
