#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL declares columns of floating point numbers by their width
"""


def test():
    """
    Declare a table with a column of floating point numbers of each width, and check its declaration
    """
    # access the package
    import pyre.db

    # a table with a column of floating point numbers of each width
    class Ratios(pyre.db.table, id="ratios"):
        # numbers of no particular width
        plain = pyre.db.float()
        # thirty two bits
        single = pyre.db.float(bits=32)
        # and sixty four
        double = pyre.db.float(bits=64)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="columns_float_sizes")
    # build the statement that creates the table
    statement = tuple(mill.createTable(table=Ratios))
    # and check it
    assert statement == (
        "CREATE TABLE ratios (",
        "  plain DOUBLE PRECISION,",
        "  single REAL,",
        "  double DOUBLE PRECISION",
        ");",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
