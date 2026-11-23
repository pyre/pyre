#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite leaves the row that is there when asked to keep it
"""


def test():
    """
    Insert a granule twice, keeping it the second time, and read it back
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="granules"):
        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # connect to a database in memory
    db = pyre.db.sqlite(name="upserts").attach()
    # make the table
    db.createTable(Granule)
    # insert a granule
    db.insert(Granule.pyre_immutable(id=1, name="first"))
    # and again, with another name, leaving to keep the row that is there
    db.insert(Granule.pyre_immutable(id=1, name="second"), existing="keep")
    # read the table back
    rows = [(row.id, row.name) for row in db.select(Granule)]
    # and check what became of the row
    assert rows == [(1, "first")], rows
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
