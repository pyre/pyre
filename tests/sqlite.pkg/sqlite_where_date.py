#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a query can compare a date field to a date in sqlite
"""


def test():
    """
    Select the rows of one day
    """
    # support
    import datetime

    # access the package
    import pyre.db

    # a table of daily readings
    class Reading(pyre.db.table, id="readings"):
        """
        One value a day
        """

        # the day
        day = pyre.db.date()
        # the value
        value = pyre.db.int()

    # the readings of one day
    class Today(pyre.db.query, reading=Reading):
        """
        The value of the nineteenth
        """

        # the field
        value = reading.value
        # the restriction
        where = reading.day == datetime.date(2026, 11, 19)

    # connect to a database in memory
    db = pyre.db.sqlite(name="where_date").attach()
    # make the table
    db.createTable(Reading)
    # with a reading on each of two days
    db.execute("INSERT INTO readings (day, value) VALUES ('2026-11-18', 1), ('2026-11-19', 2)")
    # only the one of the nineteenth qualifies
    found = [row.value for row in db.select(Today)]
    # so check
    assert found == [2], found
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
