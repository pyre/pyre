#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a column whose default is set to {NULL} declares it
"""


def test():
    """
    Declare a table with a column whose default is {NULL}, and check its declaration
    """
    # access the package
    import pyre.db

    # a table with a column whose default is explicitly {NULL}
    class Things(pyre.db.table, id="things"):
        # the name of the thing, unknown unless given
        name = pyre.db.str(maxlen=16).setDefault(pyre.db.null)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="defaults_null")
    # build the statement that creates the table
    statement = tuple(mill.createTable(table=Things))
    # and check it
    assert statement == (
        "CREATE TABLE things (",
        "  name VARCHAR(16) DEFAULT NULL",
        ");",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
