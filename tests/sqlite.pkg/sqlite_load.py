#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the records a load puts in a table come back with their values
"""


def test():
    """
    Load three records of several types, and read them back
    """
    # support
    import datetime
    import decimal

    # access the package
    import pyre.db

    # a table with columns of several types
    class Reading(pyre.db.table, id="readings"):
        """
        Readings
        """

        # the key
        id = pyre.db.int().primary()
        # a name
        name = pyre.db.str()
        # a truth value
        good = pyre.db.bool()
        # a fixed point number
        value = pyre.db.decimal(precision=6, scale=2)
        # and a date
        day = pyre.db.date()

    # the records
    records = [
        Reading.pyre_immutable(
            id=index,
            name=f"reading {index}",
            good=index % 2 == 0,
            value=decimal.Decimal(f"{index}.25"),
            day=datetime.date(2026, 11, index),
        )
        for index in range(1, 4)
    ]

    # connect to a database in memory
    db = pyre.db.sqlite(name="load").attach()
    # make the table
    db.createTable(Reading)
    # load the records
    db.load(*records)
    # read them back, in order
    rows = sorted(db.select(Reading), key=lambda row: row.id)
    # they came back with their values
    assert [tuple(row) for row in rows] == [tuple(record) for record in records], rows
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
