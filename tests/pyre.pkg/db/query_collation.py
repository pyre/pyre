#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement of a query whose rows are sorted by one of its fields
"""


def test():
    """
    Declare a table and a query sorted by the day of its readings, and check its statement
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

    # and a simple query
    class measurements(pyre.db.query, weather=Weather):
        # the city
        city = Weather.city
        # and the day
        date = Weather.date
        # the collation
        order = (date,)

    # get a server
    server = pyre.db.server()
    # generate the SQL statement
    stmt = tuple(server.sql.select(measurements))
    # and check it
    assert stmt == (
        "SELECT",
        "    weather.city AS city,",
        '    weather."date" AS "date"',
        "  FROM",
        "    weather",
        "  ORDER BY",
        '    weather."date";',
    )

    # all done
    return Weather


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
