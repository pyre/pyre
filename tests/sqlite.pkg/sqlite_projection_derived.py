#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a computed column of a query does not disturb the columns that follow it in sqlite
"""


def test():
    """
    Select a computed column between two plain ones
    """
    # access the package
    import pyre.db

    # the table of the postgres tutorial
    class Weather(pyre.db.table, id="weather"):
        """
        Temperatures by city
        """

        # the city
        city = pyre.db.str()
        # its low
        low = pyre.db.int()
        # and its high
        high = pyre.db.int()

    # the spread of each city, between its name and its high
    class Spread(pyre.db.query, weather=Weather):
        """
        How far apart the low and the high are
        """

        # the city
        city = weather.city
        # the spread, computed by the server
        spread = weather.high - weather.low
        # and the high, after it
        high = weather.high

    # connect to a database in memory
    db = pyre.db.sqlite(name="projection_derived").attach()
    # make the table
    db.createTable(Weather)
    # with one row
    db.execute("INSERT INTO weather (city, low, high) VALUES ('Chicago', 60, 85)")
    # read it through the query
    (row,) = db.select(Spread)
    # every column is what the server computed
    assert (row.city, row.spread, row.high) == ("Chicago", 25, 85), tuple(row)
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
