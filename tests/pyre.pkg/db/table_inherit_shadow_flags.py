#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a redeclared column does not take the settings of the column it replaces
"""


def test():
    """
    Derive a table that redeclares the primary key column of its base without marking it, and
    check that the derived table has no primary key
    """
    # access the package
    import pyre.db

    # a table of people
    class Person(pyre.db.table, id="persons"):
        """
        People
        """

        # the key
        id = pyre.db.int().primary()
        # and the name
        name = pyre.db.str()

    # a table of visitors, whose numbers need not be unique
    class Visitor(Person, id="visitors"):
        """
        People who visit
        """

        # the number on the visitor's pass
        id = pyre.db.int()

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="table_inherit_shadow_flags")
    # build the statement that makes the table
    statement = tuple(mill.createTable(Visitor))
    # the table has one plain number column, and the name
    assert statement == (
        "CREATE TABLE visitors",
        "  --",
        "  -- People who visit",
        "  --",
        "(",
        "  id INTEGER,",
        "  name CLOB",
        ");",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
