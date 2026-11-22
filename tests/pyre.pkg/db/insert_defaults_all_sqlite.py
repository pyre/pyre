#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of sqlite inserts a row that leaves every column to its default
"""


def test():
    """
    Insert a row that leaves every column to its default, and check the statement
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

    # a row that leaves everything to the defaults
    pet = Pet.pyre_immutable(id=Pet.default, name=Pet.default, kind=Pet.default)

    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="insert_defaults_all_sqlite")
    # build the statement
    statement = tuple(mill.insertRecords(pet))
    # and check it
    assert statement == ("INSERT INTO pets DEFAULT VALUES;",), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
