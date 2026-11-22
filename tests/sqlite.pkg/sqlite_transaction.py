#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that sqlite accepts the statements its dialect writes to begin and commit a transaction
"""


def test():
    """
    Begin a transaction, insert a row, commit it, and read the row back
    """
    # access the package
    import pyre.db

    # a table of pets
    class Pet(pyre.db.table, id="pets"):
        # the key
        id = pyre.db.int().primary()
        # the name
        name = pyre.db.str(maxlen=16, default="nameless")
        # and the kind
        kind = pyre.db.str(maxlen=16, default="cat")

    # connect to a database in memory
    db = pyre.db.sqlite(name="transaction").attach()
    # make the table
    db.createTable(Pet)
    # begin a transaction
    db.execute(*db.sql.transaction())
    # insert a row
    db.insert(Pet.pyre_immutable(id=1, name="tom", kind="cat"))
    # and commit it
    db.execute(*db.sql.commit())
    # read back what sqlite stored
    stored = db.execute("SELECT id, name, kind FROM pets").fetchall()
    # and check it
    assert stored == [(1, "tom", "cat")], stored
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
