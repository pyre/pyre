#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the literals the dialect of postgres declares as the defaults of the columns
"""


def test():
    """
    Declare a table with a column of each type postgres knows, each with a default, and check
    how the defaults are declared
    """
    # support
    import datetime
    import decimal
    import uuid

    # access the package
    import pyre.db

    # a table with a column of each type, each with a default
    class Defaults(pyre.db.table, id="defaults"):
        # truth values
        flag = pyre.db.bool(default=True)
        # integers
        count = pyre.db.int(default=7)
        # floating point numbers
        ratio = pyre.db.float(default=0.5)
        # fixed point numbers
        price = pyre.db.decimal(precision=4, scale=2, default=decimal.Decimal("12.50"))
        # text, with a quote in it
        name = pyre.db.str(maxlen=16, default="O'Hara")
        # strings of octets
        payload = pyre.db.bytes(default=b"\x00\xff")
        # dates
        day = pyre.db.date(default=datetime.date(2026, 11, 22))
        # times of day
        hour = pyre.db.time(default=datetime.time(8, 30))
        # moments
        moment = pyre.db.timestamp(default=datetime.datetime(2026, 11, 22, 8, 30))
        # identifiers
        tag = pyre.db.uuid(default=uuid.UUID("12345678-1234-5678-1234-567812345678"))
        # arrays of rank one
        row = pyre.db.array(schema=pyre.db.int(), default=(1, 2))
        # of rank two
        grid = pyre.db.array(schema=pyre.db.int(), rank=2, default=((1, 2), (3, 4)))
        # and empty ones
        empty = pyre.db.array(schema=pyre.db.int(), default=())

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="defaults_postgres")
    # build the statement that creates the table
    statement = tuple(mill.createTable(table=Defaults))
    # and check it
    assert statement == (
        "CREATE TABLE defaults (",
        "  flag BOOLEAN DEFAULT TRUE,",
        "  count INTEGER DEFAULT 7,",
        "  ratio DOUBLE PRECISION DEFAULT 0.5,",
        "  price DECIMAL(4, 2) DEFAULT 12.50,",
        "  name VARCHAR(16) DEFAULT 'O''Hara',",
        "  payload BYTEA DEFAULT '\\x00ff',",
        "  day DATE DEFAULT DATE '2026-11-22',",
        "  hour TIME DEFAULT TIME '08:30:00',",
        "  moment TIMESTAMP DEFAULT TIMESTAMP '2026-11-22 08:30:00',",
        "  tag UUID DEFAULT '12345678-1234-5678-1234-567812345678',",
        "  row INTEGER ARRAY DEFAULT ARRAY[1, 2],",
        "  grid INTEGER ARRAY DEFAULT ARRAY[ARRAY[1, 2], ARRAY[3, 4]],",
        "  empty INTEGER ARRAY DEFAULT '{}'",
        ");",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
