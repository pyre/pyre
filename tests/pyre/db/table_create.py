#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise table creation
"""


def test():
    import pyre.db

    # declare a simple table
    class Weather(pyre.db.table, id="weather"):
        """
        The sample table from the postgres tutorial
        """

        # the fields
        city = pyre.db.str()
        city.doc = "the name of the city"

        date = pyre.db.date()
        date.doc = "the date of the measurement"

        low = pyre.db.int()
        low.doc = "the low temperature"

        high = pyre.db.int()
        high.doc = "the high temperature"

        precipitation = pyre.db.float()
        precipitation.doc = "amount of rainfall"

    # get a server
    server = pyre.db.server(name="test")
    # to build the SQL statement
    stmt = tuple(server.sql.createTable(table=Weather))
    print('\n'.join(stmt))
    return

    assert stmt == (
        "CREATE TABLE weather",
        "    --",
        "    -- The sample table from the postgres tutorial",
        "    --",
        "(",
        ");"
        )
    

    return


# main
if __name__ == "__main__":
    test()


# end of file 
