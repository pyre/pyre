#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL replaces the rows that are there with MERGE
"""


def test():
    """
    Insert two granules, replacing the rows with the same keys, and check the statement
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # make a mill
    mill = pyre.db.backends.standard.mill(name="upserts")
    # build the statement
    statement = tuple(
        mill.insertRecords(
            Granule.pyre_immutable(id=1, name="first"),
            Granule.pyre_immutable(id=2, name="second"),
            existing="replace",
        )
    )
    # and check it
    assert statement == (
        "MERGE INTO granules",
        "  USING (",
        "    VALUES",
        "      (1, 'first'),",
        "      (2, 'second')",
        "  ) AS incoming (id, name)",
        "  ON (granules.id = incoming.id)",
        "  WHEN MATCHED THEN UPDATE SET",
        "    name = incoming.name",
        "  WHEN NOT MATCHED THEN INSERT (id, name)",
        "    VALUES (incoming.id, incoming.name);",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
