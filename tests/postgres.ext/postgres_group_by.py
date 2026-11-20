#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a query that groups its rows does so
"""


def test():
    """
    Select the distinct cities of a table by grouping on them
    """
    # access the package
    import pyre.db

    # the table of the postgres tutorial
    class Weather(pyre.db.table, id="pyre_group_by"):
        """
        Temperatures by city and day
        """

        # the city
        city = pyre.db.str()
        # and its high of the day
        high = pyre.db.int()

    # the cities, one row per city
    class Cities(pyre.db.query, weather=Weather):
        """
        The cities in the table
        """

        # the field
        city = weather.city
        # grouped by it
        group = weather.city

    # connect
    db = pyre.db.postgres(name="queries").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Weather)
        # with two rows for one city and one for another
        db.execute(
            "INSERT INTO pyre_group_by (city, high) VALUES"
            " ('Chicago', 80), ('Chicago', 95), ('Hayward', 70)"
        )
        # one row per city
        cities = sorted(row.city for row in db.select(Cities))
        # so check
        assert cities == ["Chicago", "Hayward"], cities
    # either way
    finally:
        # leave nothing behind
        db.execute("ROLLBACK")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
