#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres creates a table that exists already without complaint, when asked to
"""


def test():
    """
    Create a table twice, the second time allowing it to exist
    """
    # access the package
    import pyre.db

    # a table of things
    class Thing(pyre.db.table, id="pyre_exist_ok"):
        """
        Things
        """

        # the name
        name = pyre.db.str()

    # connect
    db = pyre.db.postgres(name="table_exist_ok").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Thing)
        # and again, allowing it to exist
        db.createTable(Thing, existOk=True)
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
