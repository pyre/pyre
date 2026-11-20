#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A timestamp without a format of its own writes the ISO 8601 form, which keeps the fraction of
the second and the offset, and reads it back
"""


def test() -> None:
    """
    Write a moment with a fraction of a second and an offset, and read it back
    """
    # support
    import datetime
    import pyre

    # make a schema
    schema = pyre.schemata.timestamp()
    # a zone
    zone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    # and a moment with a fraction of a second in it
    moment = datetime.datetime(2026, 11, 19, 3, 4, 5, 250000, tzinfo=zone)

    # its text keeps both
    assert schema.string(moment) == "2026-11-19 03:04:05.250000+05:30", schema.string(moment)
    # and reads back as the same moment
    assert schema.coerce(value=schema.string(moment)) == moment
    # while text without them still reads
    assert schema.coerce(value="1992-12-21 13:30:00") == datetime.datetime(1992, 12, 21, 13, 30)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
