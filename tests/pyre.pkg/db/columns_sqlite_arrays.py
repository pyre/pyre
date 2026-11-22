#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the dialect of sqlite refuses to declare a column of arrays, which sqlite has no type
for, and names the table and the column
"""


def test():
    """
    Declare a table with a column of arrays, and check the dialect of sqlite refuses it
    """
    # access the package
    import pyre.db

    # and its exceptions
    from pyre.db import exceptions

    # a table with a column of arrays
    class Things(pyre.db.table, id="things"):
        # the readings
        readings = pyre.db.array(schema=pyre.db.int(), default=None)

    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="columns_sqlite_arrays")
    # attempt to
    try:
        # build the statement that creates the table
        statement = tuple(mill.createTable(table=Things))
    # which must fail
    except exceptions.NotSupportedError as error:
        # naming the table
        assert error.table == "things", error.table
        # and the column
        assert error.column == "readings", error.column
        # in its explanation as well
        assert "things" in str(error) and "readings" in str(error), str(error)
    # if it doesn't
    else:
        # the column was declared anyway
        assert False, statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
