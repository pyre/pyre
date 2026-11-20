#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that dates and times reach python as the matching {datetime} values
"""


def test():
    """
    Read a date, a time and two timestamps through the bindings
    """
    # support
    import datetime

    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for one of each
    row = connection.exec(
        "SELECT date '2026-11-19' AS day, time '03:04:05.25' AS clock,"
        " timestamp '2026-11-19 03:04:05.25' AS naive,"
        " timestamptz '2026-11-19 03:04:05.25+00' AS aware"
    )[0]
    # the date
    assert row["day"] == datetime.date(2026, 11, 19), repr(row["day"])
    # the time of day, with its fraction of a second
    assert row["clock"] == datetime.time(3, 4, 5, 250000), repr(row["clock"])
    # the timestamp without a zone is naive
    assert row["naive"] == datetime.datetime(2026, 11, 19, 3, 4, 5, 250000), repr(row["naive"])
    # the zone of the expected instant
    utc = datetime.timezone.utc
    # the timestamp with a zone names the same instant
    assert row["aware"] == datetime.datetime(2026, 11, 19, 3, 4, 5, 250000, tzinfo=utc), repr(
        row["aware"]
    )
    # and is aware of its zone
    assert row["aware"].tzinfo is not None, repr(row["aware"])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
