#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that booleans stored in a sqlite database read back as booleans
"""


def test():
    """
    Store a true and a false value, and read them back
    """
    # access the package
    import pyre.db

    # a table of flags
    class Flag(pyre.db.table, id="flags"):
        """
        Flags
        """

        # the key
        id = pyre.db.int().primary()
        # the flag
        up = pyre.db.bool()

    # connect to a database in memory
    db = pyre.db.sqlite(name="flags").attach()
    # make the table
    db.createTable(Flag)
    # with one of each
    db.insert(Flag.pyre_immutable(id=1, up=True), Flag.pyre_immutable(id=2, up=False))
    # read them back
    flags = {row.id: row.up for row in db.select(Flag)}
    # they are truth values, not the numbers sqlite keeps them as
    assert flags[1] is True and flags[2] is False, flags
    # let go
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
