#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an upsert may detect the rows that are there by another key
"""


def test():
    """
    Insert a granule, replacing a row with the same name, and check the statement
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int().unique()
        # and the name
        name = pyre.db.str()

    # make a mill
    mill = pyre.db.backends.postgres.mill(name="upserts")
    # build the statement
    statement = tuple(
        mill.insertRecords(
            Granule.pyre_immutable(id=1, name="first"), existing="replace", key=Granule.name
        )
    )
    # and check it
    assert statement == (
        "INSERT INTO granules",
        "    (id, name)",
        "  VALUES",
        "    (1, 'first')",
        "  ON CONFLICT (name) DO UPDATE SET",
        "    id = EXCLUDED.id;",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
