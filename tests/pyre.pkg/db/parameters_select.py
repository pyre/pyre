#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection over postgres sends the value of its restriction as a parameter
"""


def test():
    """
    Restrict a query to one city, and check the city is a typed placeholder and its value
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

    # the readings of one city
    class Chicago(pyre.db.query, reading=Reading):
        # the city
        city = reading.city
        # the restriction
        where = reading.city == "Chicago"

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # build the statement
    statement = tuple(mill.select(query=Chicago, parameters=parameters))
    # the restriction holds a placeholder that says what the value is
    assert statement[-1] == "    ((reading.city) = (CAST($1 AS TEXT)));", statement[-1]
    # and the value travels beside it
    assert parameters.drain() == ("Chicago",)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
