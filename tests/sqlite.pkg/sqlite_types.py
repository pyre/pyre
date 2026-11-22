#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the values sqlite keeps in a form of its own read back in the types of their columns
"""


def test():
    """
    Store a truth value, a fixed point number, a date, a time of day and a moment, and read them
    back
    """
    # support
    import datetime
    import decimal

    # access the package
    import pyre.db

    # a table with a column of each type sqlite keeps in a form of its own
    class Things(pyre.db.table, id="things"):
        """
        Things
        """

        # the key
        id = pyre.db.int().primary()
        # truth values, which sqlite keeps as integers
        flag = pyre.db.bool()
        # fixed point numbers, which sqlite keeps as floating point ones
        price = pyre.db.decimal(precision=4, scale=2)
        # dates, which sqlite keeps as text
        day = pyre.db.date()
        # times of day
        hour = pyre.db.time()
        # and moments
        moment = pyre.db.timestamp()

    # the values: a truth value
    flag = True
    # a price
    price = decimal.Decimal("12.50")
    # a day
    day = datetime.date(2026, 11, 22)
    # an hour
    hour = datetime.time(8, 30)
    # and a moment
    moment = datetime.datetime(2026, 11, 22, 8, 30)

    # connect to a database in memory
    db = pyre.db.sqlite(name="types").attach()
    # make the table
    db.createTable(Things)
    # store the values
    db.insert(
        Things.pyre_immutable(id=1, flag=flag, price=price, day=day, hour=hour, moment=moment)
    )
    # read them back
    (thing,) = db.select(Things)
    # each one is of the type of its column: the truth value
    assert thing.flag is True, thing.flag
    # the price
    assert isinstance(thing.price, decimal.Decimal) and thing.price == price, thing.price
    # the day
    assert thing.day == day and type(thing.day) is datetime.date, thing.day
    # the hour
    assert thing.hour == hour, thing.hour
    # and the moment
    assert thing.moment == moment, thing.moment
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
