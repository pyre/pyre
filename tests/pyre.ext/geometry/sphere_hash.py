#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the bound points and shapes of the sphere hash alike when they compare equal, so they
can be members of sets and keys of dicts
"""


def test():
    """
    Make equal pairs of each kind of value and use them as members of sets and keys of dicts
    """
    # access the geometry bindings
    from pyre.extensions.pyre import geometry

    # the chart
    chart = geometry.SphereLonLat()

    # a point
    point = chart.point(longitude=10, latitude=20)
    # and another one made the same way
    again = chart.point(longitude=10, latitude=20)
    # hash alike
    assert hash(point) == hash(again)
    # so a set holds only one of them
    assert len({point, again, chart.point(longitude=20, latitude=10)}) == 2

    # two boxes made the same way
    box = geometry.SphereBox(west=170, south=-10, east=-170, north=10)
    # hash alike
    assert hash(box) == hash(geometry.SphereBox(west=170, south=-10, east=-170, north=10))

    # the corners of a small square, walked counterclockwise
    corners = [
        chart.point(longitude=x, latitude=y) for x, y in ((0, 0), (10, 0), (10, 10), (0, 10))
    ]
    # two paths through them
    path = geometry.SpherePath(vertices=corners)
    # hash alike
    assert hash(path) == hash(geometry.SpherePath(vertices=corners))
    # two rings through them
    ring = geometry.SphereRing(vertices=corners)
    # hash alike
    assert hash(ring) == hash(geometry.SphereRing(vertices=corners))
    # and a ring brought back from its reverse is the same ring, so it finds what was filed
    # under the original
    assert {ring: "square"}[geometry.orient(shape=ring.reversed())] == "square"

    # two polygons bound by the ring
    polygon = geometry.SpherePolygon(rings=[ring])
    # hash alike
    assert hash(polygon) == hash(geometry.SpherePolygon(rings=[ring]))
    # so do two unions of polygons made the same way
    assert hash(geometry.SpherePolygons(shapes=[polygon])) == hash(
        geometry.SpherePolygons(shapes=[polygon])
    )
    # and a set of shapes holds one of each
    assert len({box, path, ring, polygon, geometry.SpherePolygon(rings=[ring])}) == 4

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
