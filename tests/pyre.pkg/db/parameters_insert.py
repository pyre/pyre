#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an insert over postgres sends the values of its records as parameters
"""


def test():
    """
    Insert two records, and check their values are bare placeholders, typed by their columns
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
        # and how many there were
        count = pyre.db.int()

    # a reading
    first = Reading.pyre_immutable(city="Chicago", day=datetime.date(2026, 11, 24), count=3)
    # and another
    second = Reading.pyre_immutable(city="Boston", day=datetime.date(2026, 11, 25), count=5)
    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # build the statement
    statement = tuple(mill.insertRecords(first, second, parameters=parameters))
    # the values of the records are placeholders, numbered in order
    assert statement[-2:] == ("    ($1, $2, $3),", "    ($4, $5, $6);"), statement
    # and the values travel beside them
    assert parameters.drain() == (
        "Chicago",
        datetime.date(2026, 11, 24),
        3,
        "Boston",
        datetime.date(2026, 11, 25),
        5,
    )
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
