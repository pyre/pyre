#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that dates read the same whatever the session's {DateStyle}
"""


def test():
    """
    Read a date through a session that asked for a european, day first, style
    """
    # support
    import datetime

    # access the bindings
    from pyre.extensions import libpq

    # open a session that writes dates the european way, and in another zone
    connection = libpq.Connection(
        {"dbname": "postgres", "options": "-c DateStyle=SQL,DMY -c TimeZone=Asia/Kolkata"}
    )
    # ask for a date whose day could pass for a month
    row = connection.exec(
        "SELECT date '2026-11-02' AS day, timestamptz '2026-11-02 03:04:05+00' AS instant"
    )[0]
    # it is still the second of november
    assert row["day"] == datetime.date(2026, 11, 2), repr(row["day"])
    # the zone of the expected instant
    utc = datetime.timezone.utc
    # and the instant is still the same instant
    assert row["instant"] == datetime.datetime(2026, 11, 2, 3, 4, 5, tzinfo=utc), repr(
        row["instant"]
    )
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
