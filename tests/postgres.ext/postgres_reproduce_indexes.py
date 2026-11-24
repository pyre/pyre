#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a postgres server reproduces the indexes of the tables it reproduces
"""


def test():
    """
    Reproduce a table with an index, and look for the index in the catalog of the server
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_reproduce_indexes"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # indexed by size
    Granule.pyre_index(Granule.size)

    # the source, a sqlite database in memory
    source = pyre.db.sqlite(name="reproduce_indexes_source").attach()
    # with the table
    source.createTable(Granule)
    # and a granule
    source.insert(Granule.pyre_immutable(name="a", size=1))
    # the target
    target = pyre.db.postgres(name="reproduce_indexes").attach()
    # carefully
    try:
        # reproduce the table
        target.reproduce(source=source, tables=(Granule,))
        # the index is in the catalog
        indexes = target.run(
            "SELECT indexname FROM pg_indexes WHERE tablename = $1 AND indexname = $2",
            "pyre_reproduce_indexes",
            "pyre_reproduce_indexes_size_index",
        )
        # once
        assert len(indexes) == 1, indexes
    # either way
    finally:
        # leave nothing behind
        target.dropTable(Granule, missingOk=True)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
