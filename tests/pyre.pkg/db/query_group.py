#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a query that groups its rows says so
"""


def test():
    """
    Render a query that groups the rows of a table by city
    """
    # access the package
    import pyre.db

    # the table of the postgres tutorial
    class Weather(pyre.db.table, id="weather"):
        """
        Temperatures by city and day
        """

        # the city
        city = pyre.db.str()
        # and its high of the day
        high = pyre.db.int()

    # the cities, one row per city
    class Cities(pyre.db.query, weather=Weather):
        """
        The cities in the table
        """

        # the field
        city = weather.city
        # grouped by it
        group = weather.city

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="query_group")
    # generate the statement
    statement = tuple(mill.select(Cities))
    # and check it
    assert statement == (
        "SELECT",
        "    weather.city AS city",
        "  FROM",
        "    weather",
        "  GROUP BY",
        "    weather.city;",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
