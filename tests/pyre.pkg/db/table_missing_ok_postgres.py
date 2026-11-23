#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres drops a table only when it is present
"""


def test():
    """
    Ask the dialect of postgres to drop a table that may be gone, and check the statement
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
    statement = tuple(mill.dropTable(table=Thing, missingOk=True))
    # and check it
    assert statement == ("DROP TABLE IF EXISTS things;",), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
