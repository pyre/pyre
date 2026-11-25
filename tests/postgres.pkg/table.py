#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a table is made in the test database, and removed from it, inside a transaction block
"""

# support
import pyre.db


# a table of weather measurements
class Weather(pyre.db.table, id="weather"):
    """
    Weather measurements
    """

    # the city
    city = pyre.db.str()
    city.doc = "the city name"

    # its state
    state = pyre.db.str(maxlen=2)
    state.doc = "the state name"

    # the day of the measurement
    date = pyre.db.date()
    date.doc = "the date of the measurement"

    # the lowest temperature
    low = pyre.db.decimal(precision=5, scale=2)
    low.doc = "the temperature low"

    # and the highest
    high = pyre.db.decimal(precision=5, scale=2)
    high.doc = "the temperature high"


def test():
    """
    Make the table, find it in the catalog, remove it, and find it gone
    """
    # the statement that looks for the table in the catalog
    sql = f"SELECT tablename FROM pg_tables WHERE tablename='{Weather.pyre_name}'"

    # connect to the test database named in the local configuration file
    db = pyre.db.postgres(name="test").attach()

    # in a transaction block
    with db:
        # make the table
        db.createTable(Weather)
        # look for it; the result reads as a sequence of its rows, with the names of the columns
        # on the result rather than in its first row
        found = db.execute(sql)
        # the catalog names one column
        assert found.headers == ("tablename",)
        # and finds the table
        assert tuple(tuple(row) for row in found) == (("weather",),)
        # remove the table
        db.dropTable(Weather)
        # and find it gone
        assert tuple(db.execute(sql)) == ()

    # hand back the connection and the table
    return db, Weather


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
