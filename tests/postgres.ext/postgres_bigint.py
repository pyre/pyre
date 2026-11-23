#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a column of 64 bit integers holds a value past the range of 32 bits
"""


def test():
    """
    Store the size of a large granule, and read it back
    """
    # access the package
    import pyre.db

    # a table of granules
    class Granule(pyre.db.table, id="pyre_bigint"):
        """
        Granules and their sizes
        """

        # the key
        id = pyre.db.int().primary()
        # the size, in bytes
        size = pyre.db.int(bits=64)

    # connect
    db = pyre.db.postgres(name="bigint").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Granule)
        # ask what the column holds
        kind = db.execute(
            "SELECT data_type FROM information_schema.columns"
            " WHERE table_name = 'pyre_bigint' AND column_name = 'size'"
        )[0][0]
        # it must be a 64 bit integer
        assert kind == "bigint", kind
        # a size past the range of 32 bits
        size = 2**40 + 1
        # store it
        db.insert(Granule.pyre_immutable(id=1, size=size))
        # and read it back
        (row,) = db.select(Granule)
        # it is the same size
        assert row.size == size, row.size
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
