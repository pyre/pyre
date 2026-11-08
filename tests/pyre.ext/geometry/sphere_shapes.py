#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the bound shapes of the sphere keep what they are made of, hold the points they
should, and report their envelopes; that a ring bounds the region to its left; and that orienting
a ring makes it bound the smaller of its two regions
"""


def test():
    """
    Make each kind of shape on the sphere and look at it
    """
    # access the geometry bindings
    from pyre.extensions.pyre import geometry

    # the chart
    chart = geometry.SphereLonLat()
    # names the points of the sphere
    point = chart.point(longitude=10, latitude=20)
    # and gives back their coordinates, longitude first
    longitude, latitude = chart.coordinates(point=point)
    # to within rounding
    assert abs(longitude - 10) < 1e-12
    # in both
    assert abs(latitude - 20) < 1e-12

    # a box across the antimeridian
    box = geometry.SphereBox(west=170, south=-10, east=-170, north=10)
    # is twenty degrees wide
    assert box.width == 20
    # holds the points on either side of the antimeridian
    assert box.contains(point=chart.point(longitude=-175, latitude=0))
    # writes itself by its edges
    assert repr(box) == "SphereBox(west=170, south=-10, east=-170, north=10)"

    # the corners of a small square, walked counterclockwise
    corners = [
        chart.point(longitude=x, latitude=y) for x, y in ((0, 0), (10, 0), (10, 10), (0, 10))
    ]
    # make a ring through them
    ring = geometry.SphereRing(vertices=corners)
    # which bounds the square, to its left
    assert ring.contains(point=chart.point(longitude=5, latitude=5))
    # and not the rest of the sphere
    assert not ring.contains(point=chart.point(longitude=100, latitude=5))
    # and whose area is small
    assert ring.area < 0.1
    # walked the other way, it bounds the rest of the sphere
    outside = ring.reversed()
    # which doesn't hold the square
    assert not outside.contains(point=chart.point(longitude=5, latitude=5))
    # orienting it brings back the square
    assert geometry.orient(shape=outside) == ring

    # a polygon bound by the ring
    polygon = geometry.SpherePolygon(rings=[ring])
    # has the ring
    assert polygon.rings == [ring]
    # and an envelope around the square
    envelope = polygon.envelope()
    # from the equator
    assert abs(envelope.south) < 1e-9
    # past the latitude of the north corners, since its north edge is a great circle arc that
    # bulges toward the pole
    assert envelope.north > 10

    # a path along the equator
    path = geometry.SpherePath(
        vertices=[chart.point(longitude=0, latitude=0), chart.point(longitude=20, latitude=0)]
    )
    # has geodesic edges by default
    assert path.geodesic
    # and holds the points of the equator between its ends
    assert path.contains(point=chart.point(longitude=15, latitude=0))

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
