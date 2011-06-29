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

    # declare the table with the measurement info
    class Measurement(pyre.db.table, id="measurement"):
        """
        Weather related measurements
        """

        # the fields
        low = pyre.db.int()
        low.doc = "the low temperature"

        high = pyre.db.int()
        high.doc = "the high temperature"

        precipitation = pyre.db.float()
        precipitation.doc = "amount of rainfall"

    # check the name
    assert Measurement.pyre_name == "measurement"
    # make sure we harvested all the descriptors (and in the right order)
    assert Measurement.pyre_localColumns == tuple(
        value.column for value in (
            Measurement.low, Measurement.high, Measurement.precipitation ))
    # no inheritance here, so these should match
    assert Measurement.pyre_localColumns == Measurement.pyre_columns

    # make sure all the column descriptors know Measurement as their table
    for column in Measurement.pyre_columns:
        assert column.table == Measurement


    # now the table with the location info
    class Location(pyre.db.table, id="location"):
        """
        Location information
        """

        city = pyre.db.str()
        city.doc = "the name of the city"

        state = pyre.db.str(maxlen=2)
        state.doc = "the state"

    # check the name
    assert Location.pyre_name == "location"
    # make sure we harvested all the descriptors (and in the right order)
    assert Location.pyre_localColumns == tuple(
        value.column for value in (Location.city, Location.state))
    # no inheritance here, so these should match
    assert Location.pyre_localColumns == Location.pyre_columns

    # make sure all the column descriptors know Location as their table
    for column in Location.pyre_columns:
        assert column.table == Location


    # now put it all together
    class Weather(Location, Measurement, id="weather"):

        date = pyre.db.date()
        date.doc = "the date of the measurement"


    # check the name
    assert Weather.pyre_name == "weather"
    # make sure we harvested all the descriptors (and in the right order)
    assert Weather.pyre_localColumns == (Weather.date.column,)
    # print(Weather.pyre_columns)
    # print(tuple(column.name for column in Weather.pyre_columns))
    assert Weather.pyre_columns == tuple(
        value.column for value in (
            Weather.low, Weather.high, Weather.precipitation,
            Weather.city, Weather.state,
            Weather.date ))

    # all done
    return Measurement, Location, Weather


# main
if __name__ == "__main__":
    test()


# end of file 
