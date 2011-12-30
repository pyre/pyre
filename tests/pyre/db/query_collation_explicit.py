#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise table declaration
"""


def test():
    # access to the package
    import pyre.db

    # declare a simple table
    class Weather(pyre.db.table, id="weather"):
        """
        The sample table from the postgres tutorial
        """
        # the fields
        city = pyre.db.str()
        date = pyre.db.date()
        low = pyre.db.int()
        high = pyre.db.int()
        precipitation = pyre.db.float()

    # and a simple query
    class measurements(pyre.db.query):
        # the fields
        city = Weather.city
        date = Weather.date
        # the collation
        order = (pyre.db.ascending(date), pyre.db.descending(Weather.high))

    # get a server
    server = pyre.db.server()
    # generate the SQL statement
    stmt = tuple(server.sql.select(measurements))
    # print('\n'.join(stmt))
    assert stmt == (
        "SELECT",
        "    weather.city AS city,",
        "    weather.date AS date",
        "  FROM",
        "    weather",
        "  ORDER BY",
        "    weather.date ASC, weather.high DESC;"
        )

    # all done
    return Weather


# main
if __name__ == "__main__":
    test()


# end of file 
