#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the declaration of a table with a reference to another
"""


def test():
    """
    Declare a table that refers to another, and check the statement that creates it
    """
    # access to the package
    import pyre.db

    # the foreign table
    class City(pyre.db.table, id="cities"):
        """
        A table of cities
        """

        # the key
        id = pyre.db.int().primary()
        # the name of the city
        name = pyre.db.str()
        # and its state
        state = pyre.db.str(maxlen=2)

    # declare a simple table
    class Weather(pyre.db.table, id="weather"):
        """
        The sample table from the postgres tutorial
        """

        # the city
        city = pyre.db.reference(key=City.id)
        # the day
        date = pyre.db.date()
        # its lowest temperature
        low = pyre.db.int()
        # its highest
        high = pyre.db.int()
        # and how much it rained
        precipitation = pyre.db.float()

    # get a server
    server = pyre.db.server(name="test")
    # to build the SQL statement
    statement = tuple(server.sql.createTable(table=Weather))
    # and check it
    assert statement == (
        "CREATE TABLE weather",
        "  --",
        "  -- The sample table from the postgres tutorial",
        "  --",
        "(",
        "  city INTEGER",
        "    REFERENCES cities (id),",
        '  "date" DATE,',
        "  low INTEGER,",
        "  high INTEGER,",
        "  precipitation DOUBLE PRECISION",
        ");",
    ), statement

    # all done
    return Weather, City


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
