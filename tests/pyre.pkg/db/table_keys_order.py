#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the columns of a composite primary key keep the order they were declared in
"""


def test():
    """
    Declare a primary key of four columns, in an order other than that of the fields
    """
    # access the package
    import pyre.db

    # a table whose rows are known by two of their fields
    class Visit(pyre.db.table, id="visits"):
        """
        Who visited which city
        """

        # who
        person = pyre.db.int()
        # where
        city = pyre.db.int()
        # in which year
        year = pyre.db.int()
        # and month
        month = pyre.db.int()

    # the key runs from the coarsest to the finest, which is not the order of the fields: the year
    Visit.pyre_primaryKey(Visit.year)
    # the month
    Visit.pyre_primaryKey(Visit.month)
    # the city
    Visit.pyre_primaryKey(Visit.city)
    # and the person
    Visit.pyre_primaryKey(Visit.person)

    # get a server
    server = pyre.db.server()
    # generate the statement that makes the table
    statement = "\n".join(server.sql.createTable(Visit))
    # the key lists its columns in the order they were declared
    assert 'PRIMARY KEY ("year","month",city,person)' in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
