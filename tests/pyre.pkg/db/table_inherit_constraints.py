#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a table includes the foreign keys and the checks of the table it derives from
"""


def test():
    """
    Derive a table from one with a foreign key and a check, and check what it declares
    """
    # access the package
    import pyre.db

    # a table of cities
    class City(pyre.db.table, id="cities"):
        """
        Cities, by number
        """

        # the key
        id = pyre.db.int().primary()

    # the readings of a city
    class Reading(pyre.db.table, id="readings"):
        """
        Readings, by city
        """

        # the city
        city = pyre.db.int()
        # the low
        low = pyre.db.int()
        # and the high
        high = pyre.db.int()

    # the city is a city
    Reading.pyre_foreignKey(field=Reading.city, foreign=City.id)
    # and the low is never above the high
    Reading.pyre_check(Reading.low <= Reading.high)

    # the readings of the day, which are readings
    class Daily(Reading, id="daily"):
        """
        Readings of the day
        """

        # the day
        day = pyre.db.date()

    # make a mill that speaks standard SQL
    mill = pyre.db.backends.standard.mill(name="table_inherit_constraints")
    # build the statement that makes the derived table
    statement = "\n".join(mill.createTable(Daily))
    # it has the foreign key
    assert "FOREIGN KEY (city) REFERENCES cities (id)" in statement, statement
    # and the check, which names the fields as fields of the derived table
    assert "CHECK ((low) <= (high))" in statement, statement
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
