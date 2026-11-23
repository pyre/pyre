#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite skips rows of a selection without limiting the rest
"""


def test():
    """
    Select the readings after the first twenty, and check the statement sqlite builds
    """
    # access the package
    import pyre.db

    # a table of readings
    class Weather(pyre.db.table, id="weather"):
        # the city
        city = pyre.db.str()
        # and the day
        date = pyre.db.date()

    # the readings, by day
    class Readings(pyre.db.query, weather=Weather):
        # the city
        city = Weather.city
        # and the day
        date = Weather.date
        # in order
        order = (date,)

    # make a mill
    mill = pyre.db.backends.sqlite.mill(name="paging")
    # build the statement
    statement = tuple(mill.select(Readings, offset=20))
    # and check it
    assert statement == (
        "SELECT",
        "    weather.city AS city,",
        "    weather.date AS date",
        "  FROM",
        "    weather",
        "  ORDER BY",
        "    weather.date",
        "  LIMIT -1 OFFSET 20;",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
