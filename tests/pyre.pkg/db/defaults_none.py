#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a column declares a default only when it was given one
"""


def test():
    """
    Declare a table with a column of each type, none of them with a default, and check that the
    statement that creates it declares no defaults
    """
    # access the package
    import pyre.db

    # a table with a column of each type, none of which was given a default
    class Plain(pyre.db.table, id="plain"):
        # truth values
        flag = pyre.db.bool()
        # integers
        count = pyre.db.int()
        # floating point numbers
        ratio = pyre.db.float()
        # fixed point numbers
        price = pyre.db.decimal(precision=4, scale=2)
        # text
        name = pyre.db.str(maxlen=16)
        # strings of octets
        payload = pyre.db.bytes()
        # dates
        day = pyre.db.date()
        # times of day
        hour = pyre.db.time()
        # moments
        moment = pyre.db.timestamp()
        # and arrays
        row = pyre.db.array(schema=pyre.db.int())

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="defaults_none")
    # build the statement that creates the table
    statement = tuple(mill.createTable(table=Plain))
    # and check it
    assert statement == (
        "CREATE TABLE plain (",
        "  flag BOOLEAN,",
        '  "count" INTEGER,',
        "  ratio DOUBLE PRECISION,",
        "  price DECIMAL(4, 2),",
        "  name VARCHAR(16),",
        "  payload BLOB,",
        '  "day" DATE,',
        '  "hour" TIME,',
        "  moment TIMESTAMP,",
        '  "row" INTEGER ARRAY',
        ");",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
