#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the relations a search asks of the timeline: a window, possibly open on either side,
meets a single acquisition when they overlap at all, and meets a pair when it meets either of
its acquisitions
"""

# externals
import datetime

# support
import pyre


def test():
    """
    Check windows against single acquisitions and pairs
    """
    # the timeline
    timeline = pyre.geometry.timeline()
    # the start of a day
    day = datetime.datetime(2025, 10, 14)

    # the time a number of hours into the day
    def at(hours):
        """
        The time {hours} into the day
        """
        # easy enough
        return day + datetime.timedelta(hours=hours)

    # the window from six in the morning to six in the evening
    window = timeline.interval(begin=at(6), end=at(18))
    # an acquisition that straddles its start
    single = timeline.interval(begin=at(5), end=at(7))
    # meets it
    assert pyre.geometry.intersects(window, single)
    # and so does the window that is open on its start
    assert pyre.geometry.intersects(timeline.interval(end=at(18)), single)
    # but not the window that opens after the acquisition ends
    assert not pyre.geometry.intersects(timeline.interval(begin=at(8)), single)

    # a pair whose reference acquisition was a cycle earlier
    pair = pyre.geometry.union(
        timeline.interval(begin=at(-12 * 24 + 10), end=at(-12 * 24 + 11)),
        timeline.interval(begin=at(10), end=at(11)),
    )
    # meets the window through its secondary acquisition
    assert pyre.geometry.intersects(window, pair)
    # and so does a window around its reference acquisition
    assert pyre.geometry.intersects(
        timeline.interval(begin=at(-12 * 24), end=at(-12 * 24 + 12)), pair
    )
    # but a window between the two does not
    assert not pyre.geometry.intersects(timeline.interval(begin=at(-24), end=at(0)), pair)

    # the envelope of the pair is the hull of its acquisitions
    assert pair.envelope() == pyre.geometry.hull(*pair)
    # and covers the pair
    assert pyre.geometry.covers(pair.envelope(), pair)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
