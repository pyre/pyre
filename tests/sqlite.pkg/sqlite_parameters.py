#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the values sqlite receives as parameters come back as they were written
"""


def test():
    """
    Write a record with text that holds quotes, a date, a fixed point number and a truth value,
    and read it back
    """
    # support
    import datetime
    import decimal

    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # the day
        day = pyre.db.date()
        # the amount
        amount = pyre.db.decimal(precision=6, scale=2)
        # and whether it was checked
        checked = pyre.db.bool()

    # a reading whose text would end a literal early
    reading = Reading.pyre_immutable(
        city="O'Hara'); --",
        day=datetime.date(2026, 11, 24),
        amount=decimal.Decimal("3.25"),
        checked=True,
    )
    # connect to a database in memory
    db = pyre.db.sqlite(name="parameters").attach()
    # make the table
    db.createTable(Reading)
    # write the reading
    db.insert(reading)
    # read it back
    rows = [(row.city, row.day, row.amount, row.checked) for row in db.select(Reading)]
    # it is the one we wrote
    assert rows == [
        ("O'Hara'); --", datetime.date(2026, 11, 24), decimal.Decimal("3.25"), True)
    ], rows
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
