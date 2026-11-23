#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a unique constraint with a name is declared with it
"""


def test():
    """
    Declare a unique constraint with a name, and check the statement that creates its table
    """
    # access the package
    import pyre.db

    # a table of cities
    class City(pyre.db.table, id="cities"):
        # the key
        id = pyre.db.int().primary()

    # and a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.int()
        # the lowest reading
        low = pyre.db.float()
        # and the highest
        high = pyre.db.float()

    # no city has two readings with the same low
    Reading.pyre_unique(Reading.city, Reading.low, name="one_low")

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="constraints")
    # build the statement that creates the table
    statement = tuple(mill.createTable(table=Reading))
    # and check it
    assert statement == (
        "CREATE TABLE readings (",
        "  city INTEGER,",
        "  low DOUBLE PRECISION,",
        "  high DOUBLE PRECISION,",
        "",
        "  CONSTRAINT one_low UNIQUE (city,low)",
        ");",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
