#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres hands back the rows an update changes
"""


def test():
    """
    Rename one of two granules, and read back its key and its new name
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
    db = pyre.db.postgres(name="returning_update").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Granule)
        # with two granules
        db.insert(
            Granule.pyre_immutable(id=1, name="first"),
            Granule.pyre_immutable(id=2, name="second"),
        )
        # rename one, asking for its key and its new name
        rows = db.update(
            (Granule.pyre_immutable(name="renamed"), Granule.id == 2),
            returning=(Granule.id, Granule.name),
        )
        # the rows read as records of the returned fields
        changed = [(row.id, row.name) for row in rows]
        # and hold the granule as it is now
        assert changed == [(2, "renamed")], changed
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
