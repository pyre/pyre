#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a limit that is not an integer is refused before it reaches a statement
"""


def test():
    """
    Ask for a limit given as text, and check the mill refuses it
    """
    # access the package
    import pyre.db

    # a table of readings
    class Weather(pyre.db.table, id="weather"):
        # the city
        city = pyre.db.str()
        # and the day
        date = pyre.db.date()

    # the readings, by day
    class Readings(pyre.db.query, weather=Weather):
        # the city
        city = Weather.city
        # and the day
        date = Weather.date
        # in order
        order = (date,)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="paging")
    # attempt to
    try:
        # build a statement with a limit that is not a number
        statement = tuple(mill.select(Readings, limit="10; DROP TABLE weather"))
    # which must fail
    except TypeError as error:
        # because the limit is not an integer
        assert "integer" in str(error), str(error)
    # if it doesn't
    else:
        # the text reached the statement
        assert False, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
