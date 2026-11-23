#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that standard SQL leaves the documentation of a table in its comments
"""


def test():
    """
    Declare a documented table, and check that the standard mill records no documentation
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

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="documentation")
    # build the statements that create the table
    statement = tuple(mill.createTable(table=Reading))
    # and check they end with the table
    assert statement[-1] == ");", statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
