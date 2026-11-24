#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite stores and reads tables and columns whose names need quoting
"""


def test():
    """
    Make a table with a space in its name and columns named after keywords, write a row, and
    read it back
    """
    # access the package
    import pyre.db

    # a table whose name holds a space
    class Order(pyre.db.table, id="pyre orders"):
        # a column named after a keyword
        order = pyre.db.int().primary()
        # and another
        group = pyre.db.str()

    # connect to a database in memory
    db = pyre.db.sqlite(name="reserved_names").attach()
    # make the table
    db.createTable(Order)
    # write a row
    db.insert(Order.pyre_immutable(order=1, group="first"))
    # read it back
    rows = [(row.order, row.group) for row in db.select(Order)]
    # it is the row we wrote
    assert rows == [(1, "first")], rows
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
