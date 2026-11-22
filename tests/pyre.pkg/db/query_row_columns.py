#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a row of a query takes each of its fields from its own column, derived or not
"""


def test():
    """
    Build a row of a query with a derived column between two plain ones
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

    # build a row from the columns the server would send
    row = Spread.pyre_immutable(data=("Chicago", 25, 85))
    # every field is its own column
    assert (row.city, row.spread, row.high) == ("Chicago", 25, 85), tuple(row)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
