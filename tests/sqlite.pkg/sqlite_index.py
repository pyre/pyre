#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite creates the indexes of a table along with it
"""


def test():
    """
    Create a table with an index, and find the index in the catalog of the database
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the name
        name = pyre.db.str()

    # no two granules share a name
    Granule.pyre_index(Granule.name, unique=True)

    # connect to a database in memory
    db = pyre.db.sqlite(name="index").attach()
    # make the table, and its index
    db.createTable(Granule)
    # ask the catalog for the indexes of the table
    indexes = db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'index' AND tbl_name = 'granules'"
    ).fetchall()
    # there is one, with the name we expect
    assert indexes == [("granules_name_index",)], indexes
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
