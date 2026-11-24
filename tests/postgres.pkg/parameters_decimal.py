#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a fixed point value compared to an integer column is read as a number
"""


def test():
    """
    Select the readings whose count exceeds a fixed point value
    """
    # support
    import decimal

    # access the package
    import pyre.db

    # a table of readings
    class Reading(pyre.db.table, id="pyre_parameters_readings"):
        # the city
        city = pyre.db.str()
        # and how many there were
        count = pyre.db.int()

    # the readings above three and a half
    class Busy(pyre.db.query, reading=Reading):
        # the city
        city = reading.city
        # the restriction
        where = reading.count > decimal.Decimal("3.5")

    # connect
    db = pyre.db.postgres(name="parameters").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Reading)
        # write two readings
        db.insert(
            Reading.pyre_immutable(city="Chicago", count=3),
            Reading.pyre_immutable(city="Boston", count=5),
        )
        # select the busy ones
        rows = [row.city for row in db.select(Busy)]
        # only one is
        assert rows == ["Boston"], rows
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
