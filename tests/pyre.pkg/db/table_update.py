#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise updating rows in tables
"""


def test():
    """
    Update the phone number and birthday of one person, and check the statement
    """
    # access the package
    import pyre.db

    # declare the person table
    class Person(pyre.db.table, id="persons"):
        # the key
        id = pyre.db.int().primary()
        # the name, which is required
        name = pyre.db.str().notNull()
        # the phone number, which is required too
        phone = pyre.db.str().notNull()
        # and the birthday
        birthday = pyre.db.str()

    # initialize a person template
    eva = pyre.db.template(Person)
    # record some assignments: her phone number
    eva.phone = "1 800 555 7687"
    # and her birthday
    eva.birthday = "1930/10/28"

    # get a server
    server = pyre.db.server(name="test")
    # generate the SQL statement that updates the customer table
    statement = tuple(
        server.sql.updateRecords(template=eva, condition=(Person.name == "Eva Lu Ator"))
    )
    # and check it
    assert statement == (
        "UPDATE persons",
        "  SET",
        "    phone = '1 800 555 7687',",
        "    birthday = '1930/10/28'",
        "  WHERE ((name) = ('Eva Lu Ator'));",
    ), statement

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
