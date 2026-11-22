#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check the literals the dialect of postgres writes for times of day and moments that carry their offsets
"""


def test():
    """
    Render a time of day and a moment, each with an offset, as literals of the dialect of postgres
    """
    # support
    import datetime

    # access the package
    import pyre.db

    # the offset of india
    india = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

    # make a mill that speaks the dialect of postgres
    mill = pyre.db.dialects.postgres(name="literals_zones_postgres")
    # get its renderer of literals
    literals = mill.literals(mill=mill)

    # render a time of day with its offset
    literal = literals.value(value=datetime.time(8, 34, 5, tzinfo=india))
    # and check it
    assert literal == "TIME WITH TIME ZONE '08:34:05+05:30'", literal

    # render a moment with its offset
    literal = literals.value(value=datetime.datetime(2026, 11, 19, 8, 34, 5, tzinfo=india))
    # and check it
    assert literal == "TIMESTAMP WITH TIME ZONE '2026-11-19 08:34:05+05:30'", literal

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
