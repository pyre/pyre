#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the clauses of a query follow its tables in the order the language puts them, and
that only the last one ends the statement
"""


def test():
    """
    Render a query that restricts, groups and sorts
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

    # the warm cities, one row per city, in order
    class Warm(pyre.db.query, weather=Weather):
        """
        The cities that were ever warm
        """

        # the field
        city = weather.city
        # the restriction
        where = weather.high > 90
        # the grouping
        group = weather.city
        # and the order
        order = weather.city

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="query_clauses_order")
    # generate the statement
    statement = tuple(mill.select(Warm))
    # and check it
    assert statement == (
        "SELECT",
        "    weather.city AS city",
        "  FROM",
        "    weather",
        "  WHERE",
        "    ((weather.high) > (90))",
        "  GROUP BY",
        "    weather.city",
        "  ORDER BY",
        "    weather.city;",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
