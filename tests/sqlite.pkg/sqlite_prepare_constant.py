#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a constant next to a slot in a prepared statement keeps its value at every run
"""


def test():
    """
    Prepare the lookup of the granules of one kind by size, and run it for two sizes
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # the kind
        kind = pyre.db.str()
        # and the size
        size = pyre.db.int()

    # the raw granules of the size given when the statement runs
    class Raw(pyre.db.query, granule=Granule):
        """
        The names of the raw granules of one size
        """

        # the name
        name = granule.name
        # the restriction: a constant, and a slot
        where = (granule.kind == "raw") & (
            granule.size == pyre.db.parameter(name="size", schema=pyre.db.int())
        )

    # connect to a database in memory
    db = pyre.db.sqlite(name="prepare_constant").attach()
    # make the table
    db.createTable(Granule)
    # with granules of two kinds and two sizes
    db.insert(
        Granule.pyre_immutable(name="a", kind="raw", size=1),
        Granule.pyre_immutable(name="b", kind="raw", size=2),
        Granule.pyre_immutable(name="c", kind="cooked", size=1),
    )
    # prepare the lookup
    lookup = db.prepareSelect(query=Raw)
    # the raw granules of size one
    assert [row.name for row in lookup.run(size=1)] == ["a"]
    # and of size two
    assert [row.name for row in lookup.run(size=2)] == ["b"]
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
