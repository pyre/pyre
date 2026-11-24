#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that postgres selects and compares the casts of its dialect
"""


def test():
    """
    Select the numbers of the things whose code is greater than three
    """
    # access the package
    import pyre.db

    # a table of things, known by codes that are text
    class Thing(pyre.db.table, id="pyre_cast"):
        """
        Things, by code
        """

        # the code
        code = pyre.db.str(maxlen=8)

    # the numbers of the things whose code is greater than three
    class Numbers(pyre.db.query, thing=Thing):
        """
        The codes of the things, as numbers
        """

        # the number
        number = pyre.db.cast(thing.code, pyre.db.int())
        # the restriction
        where = pyre.db.cast(thing.code, pyre.db.int()) > 3

    # connect
    db = pyre.db.postgres(name="cast").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Thing)
        # with a few things in it
        db.execute("INSERT INTO pyre_cast (code) VALUES ('1'), ('5'), ('9')")
        # select the numbers
        found = sorted(row.number for row in db.select(Numbers))
        # and check them
        assert found == [5, 9], found
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
