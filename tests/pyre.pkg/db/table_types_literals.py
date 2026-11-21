#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the SQL literals of the values of columns: dates, times and moments as their quoted
text, octets as hexadecimal digits, identifiers in their canonical form, and arrays level by
level, with their text quoted the way SQL quotes it
"""


def test():
    """
    Render a value of each type, and check its literal
    """
    # support
    import datetime
    import uuid

    # access the package
    import pyre.db

    # a time zone
    utc = datetime.timezone.utc
    # each column, a value, and the literal it must render
    cases = [
        # a date
        (pyre.db.date(), datetime.date(2026, 11, 21), "'2026-11-21'"),
        # a date written as text
        (pyre.db.date(), "2026-11-21", "'2026-11-21'"),
        # a time of day, with its fraction of a second
        (pyre.db.time(), datetime.time(6, 30, 15, 250000), "'06:30:15.250000'"),
        # a time of day with its offset
        (
            pyre.db.time(timezone=True),
            datetime.time(6, 30, tzinfo=utc),
            "'06:30:00+00:00'",
        ),
        # a moment
        (
            pyre.db.timestamp(),
            datetime.datetime(2026, 11, 21, 6, 30),
            "'2026-11-21 06:30:00'",
        ),
        # a moment in a time zone
        (
            pyre.db.timestamp(timezone=True),
            datetime.datetime(2026, 11, 21, 6, 30, tzinfo=utc),
            "'2026-11-21 06:30:00+00:00'",
        ),
        # octets, including a zero and a quote
        (pyre.db.bytes(), b"\x00'", "'\\x0027'"),
        # an identifier
        (pyre.db.uuid(), uuid.UUID(int=1), "'00000000-0000-0000-0000-000000000001'"),
        # a matrix of integers
        (
            pyre.db.array(schema=pyre.db.int()),
            ((1, 2), (3, 4)),
            "ARRAY[ARRAY[1, 2], ARRAY[3, 4]]",
        ),
        # strings with a quote, and with nothing in them
        (pyre.db.array(schema=pyre.db.str()), ("it's", ""), "ARRAY['it''s', '']"),
        # and an empty array, which takes the type of its column
        (pyre.db.array(schema=pyre.db.int()), (), "'{}'"),
    ]
    # go through them
    for column, value, literal in cases:
        # each one renders its literal
        assert column.sql(value=value) == literal, (column.sql(value=value), literal)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
