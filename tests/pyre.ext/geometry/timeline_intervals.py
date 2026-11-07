#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the bound intervals of the timeline keep their ends, hold the instants between
them, are unbounded on the sides with an infinite end, and are empty when their ends are out of
order
"""


def test():
    """
    Make intervals of the timeline and look at them
    """
    # access the geometry bindings
    from pyre.extensions.pyre import geometry

    # a timeline
    timeline = geometry.Timeline()
    # an interval on it
    interval = timeline.interval(lower=10, upper=20)
    # knows its lower end
    assert interval.lower.coordinate == 10
    # and its upper one
    assert interval.upper.coordinate == 20
    # holds the lower one
    assert interval.contains(point=timeline.point(coordinate=10))
    # and the upper one
    assert interval.contains(point=timeline.point(coordinate=20))
    # but nothing beyond them
    assert not interval.contains(point=timeline.point(coordinate=21))
    # is bounded on both sides
    assert interval.boundedBelow and interval.boundedAbove
    # is its own envelope
    assert interval.envelope() == interval
    # and writes itself by its ends
    assert repr(interval) == "[10, 20]"

    # an interval with an infinite lower end
    until = timeline.interval(lower=float("-inf"), upper=20)
    # is unbounded below only
    assert not until.boundedBelow and until.boundedAbove
    # the whole line
    line = geometry.TimelineInterval.line()
    # is unbounded on both sides
    assert not line.boundedBelow and not line.boundedAbove

    # an interval with its ends out of order
    backwards = timeline.interval(lower=20, upper=10)
    # is empty
    assert backwards.empty
    # and the same as the empty interval
    assert backwards == geometry.TimelineInterval()
    # and writes itself as the empty set
    assert repr(backwards) == "{}"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
