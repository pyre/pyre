#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that arrays are declared as arrays of their entries, and are stored and read back with
the same entries: numbers, nested levels, text that is awkward to quote, and nothing at all
"""


def test():
    """
    Store arrays of integers and of strings, and read them back
    """
    # access the package
    import pyre.db

    # a table of arrays
    class Grid(pyre.db.table, id="pyre_array"):
        """
        Values in arrays
        """

        # the key
        id = pyre.db.int().primary()
        # a matrix of integers
        cells = pyre.db.array(schema=pyre.db.int(), rank=2)
        # and a list of labels
        labels = pyre.db.array(schema=pyre.db.str())

    # connect
    db = pyre.db.postgres(name="arrays").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Grid)
        # ask what the columns hold
        kinds = db.execute(
            "SELECT column_name, udt_name FROM information_schema.columns"
            " WHERE table_name = 'pyre_array' ORDER BY column_name"
        )
        # they must be arrays of their entries
        assert [tuple(row) for row in kinds] == [
            ("cells", "_int4"),
            ("id", "int4"),
            ("labels", "_text"),
        ], kinds
        # a matrix
        cells = ((1, 2), (3, 4))
        # and labels that are awkward to quote, including one with nothing in it
        labels = ("plain", "it's", 'a "quoted" word', "a, b", "")
        # store them
        db.insert(Grid.pyre_immutable(id=1, cells=cells, labels=labels))
        # along with a row whose arrays are empty
        db.insert(Grid.pyre_immutable(id=2, cells=(), labels=()))
        # read them back, in order
        first, second = sorted(db.select(Grid), key=lambda row: row.id)
        # the matrix is the same
        assert first.cells == cells, first.cells
        # and so are the labels
        assert first.labels == labels, first.labels
        # the empty arrays come back empty
        assert second.cells == () and second.labels == (), (second.cells, second.labels)
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
