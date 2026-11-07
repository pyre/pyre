#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the bound relations and constructions answer for intervals of the timeline and
their unions, as module functions and as methods, in either order
"""


def test():
    """
    Relate intervals and unions of intervals
    """
    # access the geometry bindings
    from pyre.extensions.pyre import geometry

    # a timeline
    timeline = geometry.Timeline()
    # the two acquisitions of a pair
    reference = timeline.interval(lower=0, upper=10)
    secondary = timeline.interval(lower=100, upper=110)
    # and their union
    pair = geometry.union(shapes=[reference, secondary])
    # has both
    assert len(pair) == 2
    assert list(pair) == [reference, secondary]
    # and writes itself with the union sign
    assert repr(pair) == "[0, 10] ∪ [100, 110]"
    # its envelope spans the gap
    assert pair.envelope() == timeline.interval(lower=0, upper=110)
    # which is the hull of its members
    assert geometry.hull(a=reference, b=secondary) == pair.envelope()

    # a window around the secondary acquisition
    window = timeline.interval(lower=105, upper=200)
    # meets the pair, in either order
    assert geometry.intersects(a=pair, b=window)
    assert geometry.intersects(a=window, b=pair)
    # and as methods too
    assert pair.intersects(other=window)
    assert window.intersects(other=pair)
    # but a window in the gap does not
    gap = timeline.interval(lower=20, upper=30)
    assert not geometry.intersects(a=pair, b=gap)
    assert not gap.intersects(other=pair)

    # the pair covers its members
    assert geometry.covers(a=pair, b=reference)
    assert pair.covers(other=secondary)
    # but not the gap between them
    assert not geometry.covers(a=pair, b=pair.envelope())
    # and the envelope covers the pair
    assert geometry.covers(a=pair.envelope(), b=pair)
    assert pair.envelope().covers(other=pair)
    # as does the pair itself
    assert geometry.covers(a=pair, b=pair)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
