#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a derived table inherits the names of the constraints of its base
"""


def test():
    """
    Derive a table from one with a named check, and check the statement that creates it
    """
    # access the package
    import pyre.db

    # a table of cities
    class City(pyre.db.table, id="cities"):
        # the key
        id = pyre.db.int().primary()

    # and a table of readings
    class Reading(pyre.db.table, id="readings"):
        # the city
        city = pyre.db.int()
        # the lowest reading
        low = pyre.db.float()
        # and the highest
        high = pyre.db.float()

    # the lowest reading may not exceed the highest
    Reading.pyre_check(Reading.low <= Reading.high, name="ordered")

    # a table of the readings that were corrected
    class Corrected(Reading, id="corrected"):
        # the reason
        reason = pyre.db.str()

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="constraints")
    # build the statement that creates the derived table
    statement = tuple(mill.createTable(table=Corrected))
    # and check that it carries the named check
    assert "  CONSTRAINT ordered CHECK ((low) <= (high))" in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
