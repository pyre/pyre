#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres creates a table only when it is missing
"""


def test():
    """
    Ask the dialect of postgres to create a table that may exist, and check the statement
    """
    # access the package
    import pyre.db

    # a table of things
    class Thing(pyre.db.table, id="things"):
        # the name
        name = pyre.db.str()

    # make a mill
    mill = pyre.db.backends.postgres.mill(name="statement")
    # build the statement
    statement = tuple(mill.createTable(table=Thing, existOk=True))
    # and check it
    assert statement == ("CREATE TABLE IF NOT EXISTS things (", "  name TEXT", ");"), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
