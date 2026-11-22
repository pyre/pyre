#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a reference keeps the settings it shares with every column, such as its default
"""


def test():
    """
    Declare a reference with a default, and check the default reaches the column
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
        # the city, which is the first one unless the office says otherwise
        city = pyre.db.reference(key=City.id, default=1)

    # find the column of the city
    (city,) = (field for field in Office.pyre_fields if field.name == "city")
    # it has the default
    assert city.default == 1, city.default
    # get a server
    server = pyre.db.server()
    # generate the statement that makes the table
    statement = "\n".join(server.sql.createTable(Office))
    # and the default is declared in it
    assert "city INTEGER DEFAULT 1" in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
