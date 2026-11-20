#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a field set to {None} is stored as NULL
"""


def test():
    """
    Insert a row whose fields, other than its key, are all {None}
    """
    # access the package
    import pyre.db

    # a table with a field of every simple type
    class Sample(pyre.db.table, id="pyre_null_insert"):
        """
        A row of values that may be absent
        """

        # the key
        id = pyre.db.int().primary()
        # a string
        name = pyre.db.str()
        # an integer
        count = pyre.db.int()
        # a real number
        ratio = pyre.db.float()
        # a flag
        flag = pyre.db.bool()
        # and a date
        day = pyre.db.date()

    # connect
    db = pyre.db.postgres(name="nulls").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Sample)
        # insert a row with nothing in it but its key
        db.insert(
            Sample.pyre_immutable(id=1, name=None, count=None, ratio=None, flag=None, day=None)
        )
        # every one of its fields must be NULL
        found = db.execute(
            "SELECT name IS NULL, count IS NULL, ratio IS NULL, flag IS NULL, day IS NULL"
            " FROM pyre_null_insert WHERE id = 1"
        )
        # so check, accepting the truth whether the bindings spell it as a boolean or as text
        assert tuple(found[0]) in {(True,) * 5, ("t",) * 5}, tuple(found[0])
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
