#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a selection of a whole table names its columns
"""


def test():
    """
    Render the selection of every row of a table
    """
    # access the package
    import pyre.db

    # the sample table from the postgres tutorial
    class Weather(pyre.db.table, id="weather"):
        """
        The sample table from the postgres tutorial
        """

        # the city
        city = pyre.db.str()
        # the day
        date = pyre.db.date()
        # its low
        low = pyre.db.int()
        # its high
        high = pyre.db.int()
        # and how much it rained
        precipitation = pyre.db.float()

    # get a server
    server = pyre.db.server()
    # generate the statement
    statement = tuple(server.sql.select(Weather))
    # and check it
    assert statement == (
        "SELECT",
        "    city,",
        '    "date",',
        "    low,",
        "    high,",
        "    precipitation",
        "  FROM weather;",
    ), statement
    # all done
    return Weather


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
