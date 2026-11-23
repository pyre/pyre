#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres quotes the documentation it records
"""


def test():
    """
    Document a column with an apostrophe, and check the statement that records it
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
        city.doc = "the city's name"
        # and the lowest reading, without documentation
        low = pyre.db.float()

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.backends.postgres.mill(name="documentation")
    # build the statements that create the table
    statement = tuple(mill.createTable(table=Reading))
    # and check that the apostrophe is doubled
    assert "COMMENT ON COLUMN readings.city IS 'the city''s name';" in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
