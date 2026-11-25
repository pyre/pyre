#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a table that refers to another, with actions on the update and removal of the rows it
refers to, is made and removed in the test database
"""

# support
import pyre.db


# a table of locations
class Location(pyre.db.table, id="location"):
    """
    Locations
    """

    # the key
    id = pyre.db.int().primary()
    id.doc = "the unique key that identifies a location"

    # the latitude
    latitude = pyre.db.float()
    latitude.doc = "the latitude of the location"

    # and the longitude
    longitude = pyre.db.float()
    longitude.doc = "the longitude of the location"


# a table of weather measurements, each at a location
class Weather(pyre.db.table, id="weather"):
    """
    Weather measurements
    """

    # the location, which goes null when the location is removed, and back to its default when
    # its key changes
    location = pyre.db.reference(
        key=Location.id, onDelete=pyre.db.setNull, onUpdate=pyre.db.setDefault
    )
    location.doc = "the location of the measurements"

    # the day of the measurement
    date = pyre.db.date()
    date.doc = "the date of the measurement"

    # the lowest temperature
    low = pyre.db.decimal(precision=5, scale=2)
    low.doc = "the temperature low"

    # and the highest
    high = pyre.db.decimal(precision=5, scale=2)
    high.doc = "the temperature high"


def queryForTable(db, table):
    """
    Interrogate the table of tables looking for {table}, and return the names it found
    """
    # build the statement
    sql = f"SELECT tablename FROM pg_tables WHERE tablename='{table.pyre_name}'"
    # execute it, and hand back its rows as plain tuples
    return tuple(tuple(row) for row in db.execute(sql))


def test():
    """
    Make both tables, the one referred to first, and remove them in the opposite order
    """
    # connect to the test database named in the local configuration file
    db = pyre.db.postgres(name="test").attach()

    # keep the notices of the server out of the output
    db.execute("SET client_min_messages = warning;")
    # in a transaction block
    with db:
        # make the table of locations
        db.createTable(Location)
        # and find it there
        assert queryForTable(db, Location) == ((Location.pyre_name,),)

        # make the table of measurements, which refers to it
        db.createTable(Weather)
        # and find it there
        assert queryForTable(db, Weather) == ((Weather.pyre_name,),)

        # remove the table of measurements
        db.dropTable(Weather)
        # and find it gone
        assert queryForTable(db, Weather) == ()

        # remove the table of locations
        db.dropTable(Location)
        # and find it gone too
        assert queryForTable(db, Location) == ()

    # hand back the connection and the tables
    return db, Weather, Location


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
