#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared selection whose bounds are slots pages through the rows
"""


def test():
    """
    Prepare a selection of the granules in order, a page at a time, and read two pages
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_prepare_paging"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # the granules, in the order of their names
    class Ordered(pyre.db.query, granule=Granule):
        """
        The names of the granules, in order
        """

        # the name
        name = granule.name
        # in order
        order = (name,)

    # connect
    db = pyre.db.postgres(name="prepare_paging").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add five granules
        db.insert(*(Granule.pyre_immutable(name=name, size=0) for name in "edcba"))
        # prepare a page of the selection, whose bounds are given when the statement runs
        page = db.prepareSelect(
            query=Ordered,
            limit=pyre.db.parameter(name="limit"),
            offset=pyre.db.parameter(name="offset"),
        )
        # the first two
        assert [row.name for row in page.run(limit=2, offset=0)] == ["a", "b"]
        # and the next three
        assert [row.name for row in page.run(limit=3, offset=2)] == ["c", "d", "e"]
    # either way
    finally:
        # leave nothing behind
        db.dropTable(Granule)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
