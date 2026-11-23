#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the selection of a whole table may be limited
"""


def test():
    """
    Select the first five rows of a table, and check the statement
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
    mill = pyre.db.backends.standard.mill(name="paging")
    # build the statement
    statement = tuple(mill.select(Weather, limit=5))
    # and check it
    assert statement == (
        "SELECT",
        "    city,",
        "    date",
        "  FROM weather",
        "  FETCH FIRST 5 ROWS ONLY;",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
