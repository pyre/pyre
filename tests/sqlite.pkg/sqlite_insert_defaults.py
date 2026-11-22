#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that sqlite fills the columns its dialect leaves out of an insert with their defaults
"""


def test():
    """
    Insert rows that leave the kind to its default, and read back what sqlite stored
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
    db = pyre.db.sqlite(name="insert_defaults").attach()
    # make the table
    db.createTable(Pet)
    # insert two rows that leave the kind to its default
    db.insert(
        Pet.pyre_immutable(id=1, name="tom", kind=Pet.default),
        Pet.pyre_immutable(id=2, name="felix", kind=Pet.default),
    )
    # read back what sqlite stored
    stored = db.execute("SELECT id, name, kind FROM pets ORDER BY id").fetchall()
    # and check it
    assert stored == [(1, "tom", "cat"), (2, "felix", "cat")], stored
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
