#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that {None} in a restriction is written as the literal {NULL}
"""


def test():
    """
    Render a query that compares a date field to {None}
    """
    # support
    import datetime

    # access the package
    import pyre.db

    # a table of daily readings
    class Reading(pyre.db.table, id="readings"):
        """
        One value a day
        """

        # the day
        day = pyre.db.date()
        # the value
        value = pyre.db.int()

    # the readings of interest
    class Selected(pyre.db.query, reading=Reading):
        """
        The readings of interest
        """

        # the field
        value = reading.value
        # the restriction
        where = reading.day == None

    # make a mill
    mill = pyre.db.backends.standard.mill(name="literals_where_null")
    # generate the statement
    statement = tuple(mill.select(Selected))
    # the restriction is the last line
    assert statement[-1] == '    ((reading."day") = (NULL));', statement[-1]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
