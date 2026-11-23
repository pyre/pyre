#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres creates the indexes of a table along with it
"""


def test():
    """
    Create a table with a unique index, and find the index in the catalog of the server
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_index"):
        """
        Granules
        """

        # the name
        name = pyre.db.str()

    # no two granules share a name
    Granule.pyre_index(Granule.name, unique=True)

    # connect
    db = pyre.db.postgres(name="index").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table, and its index
        db.createTable(Granule)
        # ask the catalog for the indexes of the table
        indexes = db.execute(
            "SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'pyre_index'"
        )
        # there is one
        ((name, definition),) = indexes
        # with the name we expect
        assert name == "pyre_index_name_index", name
        # and it is unique
        assert definition.startswith("CREATE UNIQUE INDEX"), definition
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
