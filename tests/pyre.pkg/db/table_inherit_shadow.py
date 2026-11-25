#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a column redeclared by a derived table replaces the inherited one
"""


def test():
    """
    Derive a table that redeclares a column of its base, and check that the table is made with
    the redeclared column in the place of the inherited one
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
        # and the name, of any length
        name = pyre.db.str()

    # a table of people with short names
    class Badge(Person, id="badges"):
        """
        People whose names fit on a badge
        """

        # the name, short enough to fit
        name = pyre.db.str(maxlen=8)

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="table_inherit_shadow")
    # build the statement that makes the table
    statement = tuple(mill.createTable(Badge))
    # the table has the key, and one name column, the short one
    assert statement == (
        "CREATE TABLE badges",
        "  --",
        "  -- People whose names fit on a badge",
        "  --",
        "(",
        "  id INTEGER",
        "    PRIMARY KEY,",
        "  name VARCHAR(8)",
        ");",
    ), statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
