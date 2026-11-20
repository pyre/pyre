#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that declaring what happens when a referenced row goes away leaves the field in place
"""


def test():
    """
    Declare a reference with an action on delete and one on update
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
        # the city, which takes its offices with it when it goes, and renumbers them with it
        city = pyre.db.reference(key=City.id).onDelete(pyre.db.cascade).onUpdate(pyre.db.cascade)

    # the field is a field of the table
    assert "city" in (field.name for field in Office.pyre_fields), Office.pyre_fields
    # get a server
    server = pyre.db.server()
    # generate the statement that makes the table
    statement = "\n".join(server.sql.createTable(Office))
    # the action on delete is in it
    assert "ON DELETE CASCADE" in statement, statement
    # and so is the one on update
    assert "ON UPDATE CASCADE" in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
