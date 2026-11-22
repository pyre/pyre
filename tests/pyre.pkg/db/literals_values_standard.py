#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the literals standard SQL writes for the values of a row it inserts
"""


def test():
    """
    Insert a row with a value of each type, and one missing value, and check the statement
    """
    # support
    import datetime
    import decimal

    # access the package
    import pyre.db

    # a table with a column of each type
    class Things(pyre.db.table, id="things"):
        # truth values
        flag = pyre.db.bool()
        # integers
        count = pyre.db.int()
        # floating point numbers
        ratio = pyre.db.float()
        # fixed point numbers
        price = pyre.db.decimal(precision=4, scale=2)
        # text, with a quote in it
        name = pyre.db.str(maxlen=16)
        # strings of octets
        payload = pyre.db.bytes()
        # dates
        day = pyre.db.date()
        # times of day
        hour = pyre.db.time()
        # moments
        moment = pyre.db.timestamp()
        # arrays
        row = pyre.db.array(schema=pyre.db.int())
        # and one that is left without a value
        missing = pyre.db.str(maxlen=16)

    # a row with a value for each column but the last
    thing = Things.pyre_immutable(
        flag=True,
        count=7,
        ratio=0.5,
        price=decimal.Decimal("12.50"),
        name="O'Hara",
        payload=b"\x00\xff",
        day=datetime.date(2026, 11, 22),
        hour=datetime.time(8, 30),
        moment=datetime.datetime(2026, 11, 22, 8, 30),
        row=(1, 2),
    )

    # make a mill that speaks standard SQL
    mill = pyre.db.dialects.standard(name="literals_values_standard")
    # build the statement that inserts the row
    statement = tuple(mill.insertRecords(thing))
    # and check it
    assert statement == (
        "INSERT INTO things",
        "    (flag, count, ratio, price, name, payload, day, hour, moment, row, missing)",
        "  VALUES",
        "    ("
        "TRUE, 7, 0.5, 12.50, 'O''Hara', X'00FF', "
        "DATE '2026-11-22', TIME '08:30:00', TIMESTAMP '2026-11-22 08:30:00', "
        "ARRAY[1, 2], NULL"
        ");",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
