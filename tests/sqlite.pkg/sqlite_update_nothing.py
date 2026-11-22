#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an update with a template that changes nothing leaves the table alone
"""


def test():
    """
    Update with a template that sets no column, and check that the row is unchanged
    """
    # access the package
    import pyre.db

    # a table of people
    class Person(pyre.db.table, id="persons"):
        # the key
        id = pyre.db.int().primary()
        # their name
        name = pyre.db.str(maxlen=16)
        # and their phone number
        phone = pyre.db.str(maxlen=16)

    # connect to a database in memory
    db = pyre.db.sqlite(name="update_nothing").attach()
    # make the table
    db.createTable(Person)
    # with one person in it
    db.execute("INSERT INTO persons (id, name, phone) VALUES (1, 'eva', '555 7687')")
    # apply a template that changes nothing
    db.update((pyre.db.template(Person), Person.id == 1))
    # read the row back
    stored = db.execute("SELECT id, name, phone FROM persons").fetchall()
    # and check that it is unchanged
    assert stored == [(1, "eva", "555 7687")], stored
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
