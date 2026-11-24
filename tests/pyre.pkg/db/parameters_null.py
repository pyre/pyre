#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a missing value is written as NULL, and sends no parameter
"""


def test():
    """
    Insert a record without a day, and check the day is NULL in the statement
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # the day of the reading
        day = pyre.db.date()
        # and how many there were
        count = pyre.db.int()

    # a reading without a day
    reading = Reading.pyre_immutable(city="Chicago", day=None, count=3)
    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # build the statement
    statement = tuple(mill.insertRecords(reading, parameters=parameters))
    # the missing day is written as such
    assert statement[-1] == "    ($1, NULL, $2);", statement[-1]
    # and only the others travel
    assert parameters.drain() == ("Chicago", 3)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
