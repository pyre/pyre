#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise table creation
"""


def test():
    """
    Declare a table with columns of several types and annotations, and render it
    """
    # access the package
    import pyre.db

    # declare a simple table
    class TypeFest(pyre.db.table, id="typefest"):
        """
        Exercise the type declarations
        """

        # the city
        city = pyre.db.str()
        city.doc = "a string of arbitrary length"
        # is the primary key
        city.primary()

        # the state
        state = pyre.db.str(maxlen=2)
        state.doc = "a string with maximum length 2"
        # is required
        state.notNull()

        # a date
        when = pyre.db.date()
        when.doc = "a date"
        # is unique across the rows
        when.unique()

        # a price
        price = pyre.db.decimal(precision=6, scale=2)
        price.doc = "a decimal"

        # and a floating point number
        pi = pyre.db.float()
        pi.doc = "a floating point number"

    # get a server
    server = pyre.db.server(name="test")
    # to build the SQL statement
    statement = tuple(server.sql.createTable(table=TypeFest))
    # and check it
    assert statement == (
        "CREATE TABLE typefest",
        "  --",
        "  -- Exercise the type declarations",
        "  --",
        "(",
        "  city CLOB -- a string of arbitrary length",
        "    PRIMARY KEY,",
        "  state VARCHAR(2) DEFAULT '' -- a string with maximum length 2",
        "    NOT NULL,",
        "  when DATE -- a date",
        "    UNIQUE,",
        "  price DECIMAL(6, 2) DEFAULT 0, -- a decimal",
        "  pi DOUBLE PRECISION DEFAULT 0.0 -- a floating point number",
        ");",
    )

    # all done
    return TypeFest


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
