#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of sqlite leaves the columns left to their defaults out of an insert, with a
statement for each set of columns
"""


def test():
    """
    Insert rows that leave different columns to their defaults, and check the statements
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

    # the rows
    pets = [
        # two that leave the kind to its default
        Pet.pyre_immutable(id=1, name="tom", kind=Pet.default),
        Pet.pyre_immutable(id=2, name="felix", kind=Pet.default),
        # and one that names everything
        Pet.pyre_immutable(id=3, name="rex", kind="dog"),
    ]

    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="insert_defaults_sqlite")
    # build the statements
    statement = tuple(mill.insertRecords(*pets))
    # and check them
    assert statement == (
        "INSERT INTO pets",
        "    (id, name)",
        "  VALUES",
        "    (1, 'tom'),",
        "    (2, 'felix');",
        "INSERT INTO pets",
        "    (id, name, kind)",
        "  VALUES",
        "    (3, 'rex', 'dog');",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
