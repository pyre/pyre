#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the values of a list a field is tested against are parameters, cast to their type
"""


def test():
    """
    Test a field against a list of dates, and check each date is a placeholder cast to a date
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

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="parameters")
    # and a place for the values of a statement
    parameters = mill.parameters()
    # the readings of one of two days
    predicate = pyre.db.isIn(
        Reading.day, (datetime.date(2026, 11, 22), datetime.date(2026, 11, 23))
    )
    # render it
    text = mill.expression(root=predicate, context=Reading, parameters=parameters)
    # each day is a placeholder that says it is a date
    assert text == "day IN (CAST($1 AS DATE), CAST($2 AS DATE))", text
    # and the days travel beside them
    assert parameters.drain() == (datetime.date(2026, 11, 22), datetime.date(2026, 11, 23))
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
