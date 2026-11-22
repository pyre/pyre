#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the arrays postgres sends back become tuples, at every rank
"""


def test():
    """
    Store an array of rank one and one of rank two, and read them back through a table
    """
    # access the package
    import pyre.db

    # a table of arrays
    class Grid(pyre.db.table, id="pyre_select_arrays"):
        """
        Arrays, by number
        """

        # the key
        id = pyre.db.int().primary()
        # an array of rank one
        row = pyre.db.array(schema=pyre.db.int())
        # and one of rank two
        grid = pyre.db.array(schema=pyre.db.int(), rank=2)

    # connect
    db = pyre.db.postgres(name="arrays").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Grid)
        # store one row
        db.insert(Grid.pyre_immutable(id=1, row=(1, 2), grid=((1, 2), (3, 4))))
        # read it back
        (stored,) = db.select(Grid)
        # the array of rank one is a tuple
        assert stored.row == (1, 2), stored.row
        # and so is the one of rank two, all the way down
        assert stored.grid == ((1, 2), (3, 4)), stored.grid
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
