#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the offsets of times with a zone reach python, including the seconds of the offsets
of local mean time
"""


def test():
    """
    Read a {timetz} and a {timestamptz} from the age of local mean time
    """
    # support
    import datetime

    # access the bindings
    from pyre.extensions import libpq

    # open a session in a zone whose early offset has seconds
    connection = libpq.Connection({"dbname": "postgres", "options": "-c TimeZone=Asia/Kolkata"})
    # ask for a time with an offset, and a moment from before the zone was standardized
    row = connection.exec(
        "SELECT timetz '03:04:05+05:30' AS clock, timestamptz '1850-01-01 00:00:00+00' AS early"
    )[0]
    # the offset the time was written with
    offset = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    # is the one it carries
    assert row["clock"] == datetime.time(3, 4, 5, tzinfo=offset), repr(row["clock"])
    # the moment, as written
    utc = datetime.timezone.utc
    # is the same moment, whatever offset the session wrote it in
    assert row["early"] == datetime.datetime(1850, 1, 1, tzinfo=utc), repr(row["early"])
    # and that offset has seconds in it
    assert row["early"].utcoffset().seconds % 60 != 0, repr(row["early"])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
