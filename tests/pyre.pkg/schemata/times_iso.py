#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A time without a format of its own writes the ISO 8601 form, which keeps the fraction of the
second and the offset, and reads it back
"""


def test() -> None:
    """
    Write a time with a fraction of a second and an offset, and read it back
    """
    # support
    import datetime
    import pyre

    # make a schema
    schema = pyre.schemata.time()
    # a zone
    zone = datetime.timezone(datetime.timedelta(hours=-7))
    # and a time with a fraction of a second in it
    clock = datetime.time(3, 4, 5, 250000, tzinfo=zone)

    # its text keeps both
    assert schema.string(clock) == "03:04:05.250000-07:00", schema.string(clock)
    # and reads back as the same time
    assert schema.coerce(value=schema.string(clock)) == clock
    # while text without them still reads
    assert schema.coerce(value="13:30:00") == datetime.time(13, 30)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
