#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres stores and reads tables and columns whose names need quoting
"""


def test():
    """
    Make a table with a capital in its name and columns named after reserved words, write a row,
    and read it back
    """
    # access the package
    import pyre.db

    # a table whose name keeps its capital
    class Order(pyre.db.table, id="PyreOrders"):
        """
        Orders
        """

        # a column named after a reserved word
        order = pyre.db.int().primary()
        # and another
        group = pyre.db.str()

    # connect
    db = pyre.db.postgres(name="reserved_names").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Order)
        # write a row
        db.insert(Order.pyre_immutable(order=1, group="first"))
        # read it back
        rows = [(row.order, row.group) for row in db.select(Order)]
        # it is the row we wrote
        assert rows == [(1, "first")], rows
        # and the table kept its name
        ((name,),) = db.execute("SELECT relname FROM pg_class WHERE relname = 'PyreOrders'")
        # as it was given
        assert name == "PyreOrders", name
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
