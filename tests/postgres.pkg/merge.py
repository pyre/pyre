#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the MERGE standard SQL writes for an upsert runs on postgres
"""


def test():
    """
    Merge two granules into a table that holds one of them, with the statement of the standard
    mill, and read the table back
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_merge"):
        """
        Granules
        """

        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="merge_mill")
    # connect
    db = pyre.db.postgres(name="merge_server").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Granule)
        # with one granule in it
        db.insert(Granule.pyre_immutable(id=1, name="first"))
        # build the statement that merges a new version of it and another one
        statement = mill.insertRecords(
            Granule.pyre_immutable(id=1, name="renamed"),
            Granule.pyre_immutable(id=2, name="second"),
            existing="replace",
        )
        # and run it on postgres
        db.execute(*statement)
        # read the table back
        rows = sorted((row.id, row.name) for row in db.select(Granule))
        # the first granule was written over, and the second added
        assert rows == [(1, "renamed"), (2, "second")], rows
    # either way
    finally:
        # leave nothing behind
        db.execute("ROLLBACK")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
