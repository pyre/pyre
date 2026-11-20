#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a query can select the rows whose field is NULL
"""


def test():
    """
    Select the rows with no name
    """
    # access the package
    import pyre.db

    # a table of things, some without a name
    class Thing(pyre.db.table, id="pyre_where_null"):
        """
        Things, named or not
        """

        # the key
        id = pyre.db.int().primary()
        # the name
        name = pyre.db.str()

    # the things without a name
    class Nameless(pyre.db.query, thing=Thing):
        """
        The things nobody named
        """

        # the field
        id = thing.id
        # the restriction
        where = pyre.db.isNull(thing.name)

    # connect
    db = pyre.db.postgres(name="queries").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Thing)
        # with a named row and a nameless one
        db.execute("INSERT INTO pyre_where_null (id, name) VALUES (1, 'x'), (2, NULL)")
        # only the nameless one qualifies
        found = [row.id for row in db.select(Nameless)]
        # so check
        assert found == [2], found
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
