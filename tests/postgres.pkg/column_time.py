#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a time of day is stored and read back as a time of day
"""


def test():
    """
    Store a time of day, and read it back
    """
    # support
    import datetime

    # access the package
    import pyre.db

    # a table of moments in the day
    class Alarm(pyre.db.table, id="pyre_time"):
        """
        When to wake up
        """

        # the key
        id = pyre.db.int().primary()
        # the time of day
        clock = pyre.db.time()

    # connect
    db = pyre.db.postgres(name="times").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Alarm)
        # ask what the column holds
        kind = db.execute(
            "SELECT data_type FROM information_schema.columns"
            " WHERE table_name = 'pyre_time' AND column_name = 'clock'"
        )[0][0]
        # it must be a time of day
        assert kind.startswith("time without"), kind
        # pick one
        clock = datetime.time(6, 30, 15)
        # store it
        db.insert(Alarm.pyre_immutable(id=1, clock=clock))
        # and read it back
        (alarm,) = db.select(Alarm)
        # it is the same time
        assert alarm.clock == clock, alarm.clock
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
