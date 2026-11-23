#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a query that asks for distinct rows is selected with DISTINCT
"""


def test():
    """
    Declare a query of distinct rows, and check the opening of its selection
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
        # once each
        distinct = True

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="paging")
    # build the statement
    statement = tuple(mill.select(Readings))
    # and check it opens with the request for distinct rows
    assert statement[0] == "SELECT DISTINCT", statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
