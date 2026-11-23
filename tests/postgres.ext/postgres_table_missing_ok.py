#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres drops a table that is not there without complaint, when asked to
"""


def test():
    """
    Drop a table that was never made, allowing it to be missing
    """
    # access the package
    import pyre.db

    # a table of things that is never made
    class Thing(pyre.db.table, id="pyre_missing_ok"):
        """
        Things
        """

        # the name
        name = pyre.db.str()

    # connect
    db = pyre.db.postgres(name="table_missing_ok").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # drop the table, allowing it to be missing
        db.dropTable(Thing, missingOk=True)
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
