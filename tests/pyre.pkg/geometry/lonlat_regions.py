#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the regions a search asks about: a ring walked clockwise bounds the complement of what it
encloses until it is oriented, a polygon around a pole holds the pole, and the footprint of a
frame, a union of polygons, meets a point, a box, a line and a polygon when it should
"""

# support
import pyre


def test():
    """
    Orient rings, go around a pole, and relate a footprint to the shapes of a search
    """
    # the chart
    chart = pyre.geometry.lonlat()
    # a point inside the square of the next rings
    center = chart.point(longitude=5, latitude=5)

    # a square drawn clockwise, the way the footprints of the track/frame database are
    clockwise = chart.polygon(rings=[[(0, 0), (0, 10), (10, 10), (10, 0)]])
    # bounds the rest of the sphere, since a ring bounds the region to its left
    assert not clockwise.contains(point=center)
    # until it is oriented
    oriented = pyre.geometry.orient(clockwise)
    # after which it bounds the square
    assert oriented.contains(point=center)
    # and orienting a polygon that already bounds the smaller region leaves it alone
    assert pyre.geometry.orient(oriented) == oriented

    # a polygon around the north pole, drawn as a person would, in any direction
    arctic = pyre.geometry.orient(chart.polygon(rings=[[(0, 80), (270, 80), (180, 80), (90, 80)]]))
    # holds the pole
    assert arctic.contains(point=chart.point(longitude=0, latitude=90))
    # and the points near it on every side
    assert arctic.contains(point=chart.point(longitude=-179, latitude=85))
    # but not the equator
    assert not arctic.contains(point=center)

    # the footprint of a frame on the antimeridian, cut in two along it, with edges straight in
    # the chart
    footprint = pyre.geometry.union(
        chart.polygon(rings=[[(176, 0), (180, 0), (180, 4), (176, 4)]], geodesic=False),
        chart.polygon(rings=[[(-180, 0), (-176, 0), (-176, 4), (-180, 4)]], geodesic=False),
    )
    # holds a point on the far side of the antimeridian
    assert pyre.geometry.intersects(footprint, chart.point(longitude=-178, latitude=2))
    # meets a box that straddles it
    assert pyre.geometry.intersects(footprint, chart.box(west=179, south=1, east=-179, north=3))
    # and a line that crosses it
    line = chart.path(vertices=[(170, 2), (-170, 2)])
    # meets it
    assert pyre.geometry.intersects(line, footprint)
    # as does a polygon that overlaps one of its pieces
    region = chart.polygon(rings=[[(174, 1), (178, 1), (178, 3), (174, 3)]])
    # whichever is asked first
    assert pyre.geometry.intersects(footprint, region)
    # but not the square near the prime meridian
    assert not pyre.geometry.intersects(footprint, oriented)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
