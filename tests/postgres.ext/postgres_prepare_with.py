#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a prepared statement used as a context releases its name on the server when the block
ends
"""


def test():
    """
    Run a prepared lookup inside a block, and check the statements the session knows after it
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_prepare_with"):
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

    # the statements the session has prepared
    known = "SELECT name FROM pg_prepared_statements"
    # connect
    db = pyre.db.postgres(name="prepare_with").attach()
    # make the table
    db.createTable(Granule)
    # carefully
    try:
        # prepare the lookup for the length of a block
        with db.prepareSelect(query=Lookup) as lookup:
            # run it, which puts it on the server
            list(lookup.run(name="a"))
        # once the block is over, the server has forgotten it
        assert list(db.execute(known)) == []
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
