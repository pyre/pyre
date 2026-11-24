#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a table may have columns named after the clauses of queries, which postgres reserves,
and that a query over it still uses those words for its clauses
"""


def test():
    """
    Make a table with columns named order, where and group, write rows, and select them with a
    query whose clauses go by the same names
    """
    # access the package
    import pyre.db

    # a table whose columns are named after reserved words
    class Clauses(pyre.db.table, id="pyre_reserved"):
        """
        Columns named after the clauses of queries
        """

        # the order of a row
        order = pyre.db.int().primary()
        # where it is
        where = pyre.db.str()
        # and its group
        group = pyre.db.str()

    # a query over it, whose fields have names of their own and whose clauses keep theirs
    class Selected(pyre.db.query, row=Clauses):
        # the order of the row
        position = row.order
        # and its place
        place = row.where
        # the rows of one group
        where = row.group == "first"
        # in order
        order = (position,)

    # connect
    db = pyre.db.postgres(name="reserved").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table, which postgres accepts now that the names are quoted
        db.createTable(Clauses)
        # write two rows of one group and one of another
        db.insert(
            Clauses.pyre_immutable(order=2, where="there", group="first"),
            Clauses.pyre_immutable(order=1, where="here", group="first"),
            Clauses.pyre_immutable(order=3, where="elsewhere", group="second"),
        )
        # select the rows of the first group, in order
        rows = [(row.position, row.place) for row in db.select(Selected)]
        # they are the two of that group
        assert rows == [(1, "here"), (2, "there")], rows
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
