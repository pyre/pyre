#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that postgres pages through the rows of a selection
"""


def test():
    """
    Store five readings, and select the second and third
    """
    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="pyre_paging"):
        """
        Readings
        """

        # the day of the month
        day = pyre.db.int()

    # the readings, by day
    class Days(pyre.db.query, reading=Reading):
        # the day
        day = reading.day
        # in order
        order = (day,)

    # connect
    db = pyre.db.postgres(name="paging").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Reading)
        # with five readings
        db.insert(*(Reading.pyre_immutable(day=day) for day in (5, 3, 1, 4, 2)))
        # skip the first, and take the next two
        days = [row.day for row in db.select(Days, limit=2, offset=1)]
        # which are the second and third days
        assert days == [2, 3], days
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
