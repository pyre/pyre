#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement of a query that extends another with a computed field, and sorts by it
"""


def test():
    """
    Extend a query with the average of two fields, sort by it and by an inherited field, and check
    the statement
    """
    # access to the package
    import pyre.db

    # declare a simple table
    class Weather(pyre.db.table, id="weather"):
        """
        The sample table from the postgres tutorial
        """

        # the city
        city = pyre.db.str()
        # the day of the reading, a name the language reserves
        date = pyre.db.date()
        # the lowest temperature of the day
        low = pyre.db.int()
        # the highest
        high = pyre.db.int()
        # and the precipitation
        precipitation = pyre.db.float()

    # a simple query
    class simple(pyre.db.query, weather=Weather):
        # the city
        city = weather.city
        # and the day
        date = weather.date

    # that gets extended with a new field and a collation order
    class measurements(simple):
        # the new field
        average = (weather.high - weather.low) / 2
        # the collation order
        order = pyre.db.descending(average), simple.city

    # get a server
    server = pyre.db.server()
    # generate the SQL statement
    stmt = tuple(server.sql.select(measurements))
    # and check it
    assert stmt == (
        "SELECT",
        "    weather.city AS city,",
        '    weather."date" AS "date",',
        "    ((weather.high) - (weather.low)) / (2) AS average",
        "  FROM",
        "    weather",
        "  ORDER BY",
        "    average DESC, weather.city;",
    )

    # all done
    return Weather


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
