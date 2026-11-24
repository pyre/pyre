#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the statement of a query that draws its fields from two copies of one table
"""


def test():
    """
    Declare a table and a query over two copies of it, and check its statement
    """
    # access to the package
    import pyre.db

    # declare a simple table
    class Weather(pyre.db.table, id="weather"):
        """
        The sample table from the postgres tutorial
        """

        # the city
        city = pyre.db.str()
        # the day of the reading, a name the language reserves
        date = pyre.db.date()
        # the lowest temperature of the day
        low = pyre.db.int()
        # the highest
        high = pyre.db.int()
        # and the precipitation
        precipitation = pyre.db.float()

    # and a meaningless query from two copies of the same table
    class measurements(pyre.db.query, w1=Weather, w2=Weather):
        # the fields
        # the city, from one copy
        city = w1.city
        # and the day, from the other
        date = w2.date

    # get a server
    server = pyre.db.server()
    # generate the SQL statement
    stmt = tuple(server.sql.select(measurements))
    # and check it
    assert stmt == (
        "SELECT",
        "    w1.city AS city,",
        '    w2."date" AS "date"',
        "  FROM",
        "    weather AS w1,",
        "    weather AS w2;",
    )

    # all done
    return Weather


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
