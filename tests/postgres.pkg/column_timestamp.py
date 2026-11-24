#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an instant is stored and read back as the same instant
"""


def test():
    """
    Store an instant with a time zone and a fraction of a second, and read it back
    """
    # support
    import datetime

    # access the package
    import pyre.db

    # a table of events
    class Event(pyre.db.table, id="pyre_timestamp"):
        """
        Things that happened
        """

        # the key
        id = pyre.db.int().primary()
        # when it happened
        instant = pyre.db.timestamp(timezone=True)

    # connect
    db = pyre.db.postgres(name="times").attach()
    # in a transaction that leaves nothing behind
    db.execute("BEGIN")
    # carefully
    try:
        # make the table
        db.createTable(Event)
        # a zone other than the server's
        india = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        # and an instant written in it
        instant = datetime.datetime(2026, 11, 19, 8, 34, 5, 250000, tzinfo=india)
        # store it
        db.insert(Event.pyre_immutable(id=1, instant=instant))
        # and read it back
        (event,) = db.select(Event)
        # it is the same instant, whatever zone it comes back in
        assert event.instant == instant, event.instant
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
