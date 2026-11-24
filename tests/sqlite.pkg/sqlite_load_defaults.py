#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a load fills the columns its records leave to the server with their defaults, while
the records that give them values keep theirs
"""


def test():
    """
    Load records that leave a column to its default between records that do not
    """
    # access the package
    import pyre.db

    # a table of pets
    class Pet(pyre.db.table, id="pets"):
        """
        Pets
        """

        # the key
        id = pyre.db.int().primary()
        # the name
        name = pyre.db.str()
        # and the kind, which has a default
        kind = pyre.db.str(default="cat")

    # connect to a database in memory
    db = pyre.db.sqlite(name="load_defaults").attach()
    # make the table
    db.createTable(Pet)
    # load records that alternate between giving the kind and leaving it to its default
    db.load(
        Pet.pyre_immutable(id=1, name="tom", kind=Pet.default),
        Pet.pyre_immutable(id=2, name="rex", kind="dog"),
        Pet.pyre_immutable(id=3, name="felix", kind=Pet.default),
    )
    # read them back, in order
    rows = sorted(db.select(Pet), key=lambda row: row.id)
    # the kinds are the defaults and the given ones
    assert [(row.name, row.kind) for row in rows] == [
        ("tom", "cat"),
        ("rex", "dog"),
        ("felix", "cat"),
    ], rows
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
