#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the timeline names its instants by the civil calendar: times without a time zone are
read as UTC, times with one are converted, the times it hands back are in UTC, and the ends of
the line have no time
"""

# externals
import datetime

# support
import pyre


def test():
    """
    Go from times to instants and back
    """
    # a timeline on the unix epoch
    timeline = pyre.geometry.timeline()
    # whose epoch is the start of 1970 in UTC
    assert timeline.epoch == datetime.datetime(1970, 1, 1, tzinfo=datetime.UTC)

    # a time without a time zone
    naive = datetime.datetime(2025, 10, 14, 6, 0, 0)
    # the same time, in UTC
    utc = naive.replace(tzinfo=datetime.UTC)
    # and the same time, two hours east
    east = utc.astimezone(datetime.timezone(datetime.timedelta(hours=2)))
    # all name the same instant
    assert timeline.point(time=naive) == timeline.point(time=utc)
    assert timeline.point(time=east) == timeline.point(time=utc)
    # which is the right number of seconds past the epoch
    assert timeline.point(time=utc).coordinate == utc.timestamp()
    # and whose time is the same, in UTC
    assert timeline.time(point=timeline.point(time=east)) == utc
    # down to the microsecond
    precise = utc + datetime.timedelta(microseconds=123456)
    assert timeline.time(point=timeline.point(time=precise)) == precise

    # a timeline with an epoch of its own
    local = pyre.geometry.timeline(epoch=naive)
    # puts that epoch at its origin
    assert local.point(time=utc).coordinate == 0
    # and names the times after it by their seconds past it
    assert local.point(time=naive + datetime.timedelta(hours=1)).coordinate == 3600

    # an interval open on its start
    interval = timeline.interval(end=utc)
    # has no time for its lower end
    assert timeline.time(point=interval.lower) is None
    # but has one for its upper end
    assert timeline.time(point=interval.upper) == utc

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
