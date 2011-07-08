#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise table declaration
"""


def test():
    # access to the package
    import pyre.db

    # declare a simple table
    class Weather(pyre.db.table, id="weather"):
        """
        The sample table from the postgres tutorial
        """

        # the fields
        city = pyre.db.str()
        city.doc = "the name of the city"

        date = pyre.db.date()
        date.doc = "the date of the measurement"

        low = pyre.db.int()
        low.doc = "the low temperature"

        high = pyre.db.int()
        high.doc = "the high temperature"

        precipitation = pyre.db.float()
        precipitation.doc = "amount of rainfall"

    # check the name
    assert Weather.pyre_name == "weather"
    # make sure we harvested all the descriptors (and in the right order)
    assert Weather.pyre_localColumns == tuple(
        value.column for value in (
            Weather.city, Weather.date, Weather.low, Weather.high, Weather.precipitation
            ))

    # no inheritance here, so these should match
    assert Weather.pyre_localColumns == Weather.pyre_columns

    # make sure all the column descriptors report Weather as their table
    for column in Weather.pyre_columns:
        ref = getattr(Weather, column.name)
        assert ref.table == Weather
        assert ref.column == column

    # all done
    return Weather


# main
if __name__ == "__main__":
    test()


# end of file 
