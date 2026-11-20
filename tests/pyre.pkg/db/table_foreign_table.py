#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a foreign key may name a table, and refer to its primary key
"""


def test():
    """
    Declare a field that refers to a table rather than to one of its fields
    """
    # access the package
    import pyre.db

    # the table referred to
    class City(pyre.db.table, id="cities"):
        """
        Cities, by number
        """

        # the key
        id = pyre.db.int().primary()

    # and the one that refers to it
    class Office(pyre.db.table, id="offices"):
        """
        Offices, each in a city
        """

        # the key
        id = pyre.db.int().primary()
        # the city, by the key of its table
        city = pyre.db.int().references(key=City)

    # get a server
    server = pyre.db.server()
    # generate the statement that makes the table
    statement = "\n".join(server.sql.createTable(Office))
    # the field refers to the table
    assert "REFERENCES cities" in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
