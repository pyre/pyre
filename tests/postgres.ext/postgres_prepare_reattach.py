#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared statement runs again after its server attaches to a new session, which
knows none of the statements of the old one
"""


def test():
    """
    Run a prepared lookup, detach and attach the server, and run it again
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_prepare_reattach"):
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
    db = pyre.db.postgres(name="prepare_reattach").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # add a granule
        db.insert(Granule.pyre_immutable(name="a", size=1))
        # prepare the lookup
        lookup = db.prepareSelect(query=Lookup)
        # run it, which puts it on the server
        assert [row.size for row in lookup.run(name="a")] == [1]
        # hang up
        db.detach()
        # and connect again
        db.attach()
        # the lookup still runs, on the new session
        assert [row.size for row in lookup.run(name="a")] == [1]
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
