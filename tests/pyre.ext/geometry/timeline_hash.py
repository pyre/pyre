#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the bound instants, intervals and unions of intervals of the timeline hash alike
when they compare equal, so they can be members of sets and keys of dicts
"""


def test():
    """
    Make equal pairs of each kind of value and use them as members of sets and keys of dicts
    """
    # access the geometry bindings
    from pyre.extensions.pyre import geometry

    # a timeline
    timeline = geometry.Timeline()

    # two instants made the same way
    hour = timeline.point(coordinate=3600)
    again = timeline.point(coordinate=3600)
    # hash alike
    assert hash(hour) == hash(again)
    # so a set holds only one of them
    assert len({hour, again, timeline.point(coordinate=7200)}) == 2
    # and either one finds what was filed under the other
    assert {hour: "hour"}[again] == "hour"

    # two intervals made the same way
    interval = timeline.interval(lower=10, upper=20)
    copy = timeline.interval(lower=10, upper=20)
    # hash alike
    assert hash(interval) == hash(copy)
    # so a set holds only one of them
    assert len({interval, copy}) == 1
    # an interval with its ends out of order is the empty one
    backwards = timeline.interval(lower=20, upper=10)
    # so the two hash alike
    assert hash(backwards) == hash(geometry.TimelineInterval())

    # two unions made the same way
    pieces = geometry.TimelineIntervals(shapes=[interval, timeline.interval(lower=30, upper=40)])
    others = geometry.TimelineIntervals(shapes=[copy, timeline.interval(lower=30, upper=40)])
    # hash alike
    assert hash(pieces) == hash(others)
    # and either one finds what was filed under the other
    assert {pieces: "pieces"}[others] == "pieces"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
