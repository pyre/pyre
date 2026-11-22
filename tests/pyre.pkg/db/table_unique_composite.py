#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a call that marks several fields as unique makes them unique together
"""


def test():
    """
    Mark two fields as unique together, and check the constraint
    """
    # access the package
    import pyre.db

    # a table of people
    class Person(pyre.db.table, id="persons"):
        """
        People
        """

        # the name
        name = pyre.db.int()
        # the phone number
        phone = pyre.db.int()
        # and the email address
        email = pyre.db.int()

    # the name and the phone number are unique together
    Person.pyre_unique(Person.name, Person.phone)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="table_unique_composite")
    # build the statement that makes the table
    statement = "\n".join(mill.createTable(Person))
    # the pair is unique
    assert "UNIQUE (name,phone)" in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
