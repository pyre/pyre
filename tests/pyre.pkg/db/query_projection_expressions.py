#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement of a query with a field computed from others
"""


def test():
    """
    Declare a table and a query with the average of two of its fields, and check its statement
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

    # and a query with a field computed from others
    class measurements(pyre.db.query, weather=Weather):
        # the city
        city = weather.city
        # and the day
        date = weather.date
        # and the average of the day's extremes
        average = (weather.high - weather.low) / 2

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
        "    weather;",
    )

    # all done
    return Weather


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
