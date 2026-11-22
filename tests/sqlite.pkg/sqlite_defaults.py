#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that sqlite accepts the defaults its dialect declares, and fills them in
"""


def test():
    """
    Make a table with a default for each column, insert a row that names only its key, and
    read back what sqlite stored
    """
    # support
    import datetime
    import decimal

    # access the package
    import pyre.db

    # a table with a column of each type, each with a default
    class Defaults(pyre.db.table, id="defaults"):
        # the key
        id = pyre.db.int().primary()
        # truth values
        flag = pyre.db.bool(default=True)
        # integers
        count = pyre.db.int(default=7)
        # floating point numbers
        ratio = pyre.db.float(default=0.5)
        # fixed point numbers
        price = pyre.db.decimal(precision=4, scale=2, default=decimal.Decimal("12.50"))
        # text, with a quote in it
        name = pyre.db.str(maxlen=16, default="O'Hara")
        # strings of octets
        payload = pyre.db.bytes(default=b"\x00\xff")
        # dates
        day = pyre.db.date(default=datetime.date(2026, 11, 22))
        # times of day
        hour = pyre.db.time(default=datetime.time(8, 30))
        # moments
        moment = pyre.db.timestamp(default=datetime.datetime(2026, 11, 22, 8, 30))

    # connect to a database in memory
    db = pyre.db.sqlite(name="defaults").attach()
    # make the table
    db.createTable(Defaults)
    # insert a row that names only its key
    db.execute("INSERT INTO defaults (id) VALUES (1)")
    # read back what sqlite stored
    stored = db.execute(
        "SELECT flag, count, ratio, price, name, payload, day, hour, moment FROM defaults"
    ).fetchall()
    # and check it
    assert stored == [
        (1, 7, 0.5, 12.5, "O'Hara", b"\x00\xff", "2026-11-22", "08:30:00", "2026-11-22 08:30:00")
    ], stored
    # disconnect
    db.detach()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
