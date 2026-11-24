#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared selection runs as often as it is asked, each time with its own values
"""


def test():
    """
    Prepare the lookup of a granule by name, and run it for two names
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_prepare_select"):
        """
        Granules
        """

        # the name
        name = pyre.db.str().primary()
        # and the size
        size = pyre.db.int()

    # the size of the granule whose name is given when the statement runs
    class Lookup(pyre.db.query, granule=Granule):
        """
        The size of one granule
        """

        # the size
        size = granule.size
        # the restriction
        where = granule.name == pyre.db.parameter(name="name", schema=pyre.db.str())

    # connect
    db = pyre.db.postgres(name="prepare_select").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add two granules
        db.insert(
            Granule.pyre_immutable(name="a", size=1), Granule.pyre_immutable(name="b", size=2)
        )
        # prepare the lookup
        lookup = db.prepareSelect(query=Lookup)
        # look up the first
        assert [row.size for row in lookup.run(name="a")] == [1]
        # and the second
        assert [row.size for row in lookup.run(name="b")] == [2]
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
