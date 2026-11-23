#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL declares columns of integers by their width
"""


def test():
    """
    Declare a table with a column of integers of each width, and check its declaration
    """
    # access the package
    import pyre.db

    # a table with a column of integers of each width
    class Counts(pyre.db.table, id="counts"):
        # integers of no particular width
        plain = pyre.db.int()
        # sixteen bits
        small = pyre.db.int(bits=16)
        # thirty two
        medium = pyre.db.int(bits=32)
        # and sixty four
        large = pyre.db.int(bits=64)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="columns_int_sizes")
    # build the statement that creates the table
    statement = tuple(mill.createTable(table=Counts))
    # and check it
    assert statement == (
        "CREATE TABLE counts (",
        "  plain INTEGER,",
        "  small SMALLINT,",
        "  medium INTEGER,",
        "  large BIGINT",
        ");",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
