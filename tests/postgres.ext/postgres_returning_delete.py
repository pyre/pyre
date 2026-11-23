#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres hands back the rows a deletion removes
"""


def test():
    """
    Delete one of two granules, and read back its whole row
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_returning"):
        """
        Granules
        """

        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # connect
    db = pyre.db.postgres(name="returning_delete").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Granule)
        # with two granules
        db.insert(
            Granule.pyre_immutable(id=1, name="kept"),
            Granule.pyre_immutable(id=2, name="removed"),
        )
        # delete one, asking for the whole of its row
        rows = db.delete(Granule, Granule.id == 2, returning=Granule)
        # the rows read as records of the table
        gone = [(row.id, row.name) for row in rows]
        # and hold the granule that was removed
        assert gone == [(2, "removed")], gone
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
