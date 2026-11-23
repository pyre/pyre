#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres records the documentation of a table and its columns in its catalog
"""


def test():
    """
    Declare a documented table, and check the statements the dialect of postgres builds for it
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="readings"):
        """
        Daily readings, by city
        """

        # the city
        city = pyre.db.str(maxlen=32)
        city.doc = "the name of the city"
        # and the lowest reading, without documentation
        low = pyre.db.float()

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="documentation")
    # build the statements that create the table
    statement = tuple(mill.createTable(table=Reading))
    # and check them
    assert statement == (
        "CREATE TABLE readings",
        "  --",
        "  -- Daily readings, by city",
        "  --",
        "(",
        "  city VARCHAR(32), -- the name of the city",
        "  low DOUBLE PRECISION",
        ");",
        "COMMENT ON TABLE readings IS 'Daily readings, by city';",
        "COMMENT ON COLUMN readings.city IS 'the name of the city';",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
