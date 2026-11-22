#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the types the dialect of postgres declares for the columns it supports
"""


def test():
    """
    Declare a table with a column of each type postgres knows, and check its declaration
    """
    # access the package
    import pyre.db

    # a table with a column of each type, none of which has a default
    class Columns(pyre.db.table, id="columns"):
        # truth values
        flag = pyre.db.bool(default=None)
        # integers
        count = pyre.db.int(default=None)
        # floating point numbers
        ratio = pyre.db.float(default=None)
        # fixed point numbers
        price = pyre.db.decimal(precision=6, scale=2, default=None)
        # text of bounded length
        state = pyre.db.str(maxlen=2, default=None)
        # and of unbounded length
        name = pyre.db.str(default=None)
        # strings of octets
        payload = pyre.db.bytes(default=None)
        # dates
        day = pyre.db.date(default=None)
        # times of day, without their offsets
        hour = pyre.db.time(default=None)
        # and with them
        local = pyre.db.time(timezone=True, default=None)
        # moments, without their time zones
        moment = pyre.db.timestamp(default=None)
        # and with them
        instant = pyre.db.timestamp(timezone=True, default=None)
        # identifiers
        tag = pyre.db.uuid(default=None)
        # arrays of rank one
        row = pyre.db.array(schema=pyre.db.int(), default=None)
        # of rank two
        grid = pyre.db.array(schema=pyre.db.int(), rank=2, default=None)
        # and of text
        names = pyre.db.array(schema=pyre.db.str(), default=None)

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="columns_postgres")
    # build the statement that creates the table
    statement = tuple(mill.createTable(table=Columns))
    # and check it
    assert statement == (
        "CREATE TABLE columns (",
        "  flag BOOLEAN,",
        "  count INTEGER,",
        "  ratio DOUBLE PRECISION,",
        "  price DECIMAL(6, 2),",
        "  state VARCHAR(2),",
        "  name TEXT,",
        "  payload BYTEA,",
        "  day DATE,",
        "  hour TIME,",
        "  local TIME WITH TIME ZONE,",
        "  moment TIMESTAMP,",
        "  instant TIMESTAMP WITH TIME ZONE,",
        "  tag UUID,",
        "  row INTEGER ARRAY,",
        "  grid INTEGER ARRAY,",
        "  names TEXT ARRAY",
        ");",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
