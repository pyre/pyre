#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that sqlite's placeholders are numbered, and its values take the forms its literals have
"""


def test():
    """
    Insert a record with a date and a truth value, and check the placeholders and the values
    """
    # support
    import datetime

    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.str()
        # the day of the reading
        day = pyre.db.date()
        # and whether it was checked
        checked = pyre.db.bool()

    # a reading
    reading = Reading.pyre_immutable(city="Chicago", day=datetime.date(2026, 11, 24), checked=True)
    # make a mill that speaks the dialect of sqlite
    mill = pyre.db.backends.sqlite.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # build the statement
    statement = tuple(mill.insertRecords(reading, parameters=parameters))
    # the values are numbered placeholders, without casts
    assert statement[-1] == "    (?1, ?2, ?3);", statement[-1]
    # the date travels as the text sqlite keeps, and the truth value as an integer
    assert parameters.drain() == ("Chicago", "2026-11-24", 1)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
