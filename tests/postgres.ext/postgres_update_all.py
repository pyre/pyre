#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an update without a condition applies to every row, as a delete without one does
"""


def test():
    """
    Update every row of a table at once
    """
    # access the package
    import pyre.db

    # a table of counters
    class Counter(pyre.db.table, id="pyre_update_all"):
        """
        Counters that are all reset together
        """

        # the key
        id = pyre.db.int().primary()
        # the count
        count = pyre.db.int()

    # connect
    db = pyre.db.postgres(name="updates").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Counter)
        # with a few rows in it
        db.execute("INSERT INTO pyre_update_all (id, count) VALUES (1, 5), (2, 7), (3, 9)")
        # build a template that resets the count
        template = pyre.db.template(Counter)
        template.count = 0
        # apply it to every row
        db.update((template, None))
        # every count must now be zero
        counts = db.execute("SELECT count FROM pyre_update_all ORDER BY id")
        # so check
        assert [int(row[0]) for row in counts] == [0, 0, 0], [row[0] for row in counts]
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
