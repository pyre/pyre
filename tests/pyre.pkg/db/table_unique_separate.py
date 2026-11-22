#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that each call that marks fields as unique makes a constraint of its own
"""


def test():
    """
    Mark two fields as unique, one at a time, and check that each one is unique on its own
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

    # the phone number is unique
    Person.pyre_unique(Person.phone)
    # and so is the email address
    Person.pyre_unique(Person.email)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="table_unique_separate")
    # build the statement that makes the table
    statement = "\n".join(mill.createTable(Person))
    # each field is unique on its own
    assert "UNIQUE (phone),\n  UNIQUE (email)" in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
