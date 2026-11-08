#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the bound relations answer for the shapes of the sphere, as module functions and as
methods, in either order, including a union of polygons such as the footprint of a frame
"""


def test():
    """
    Relate points, boxes, paths, polygons and unions of polygons
    """
    # access the geometry bindings
    from pyre.extensions.pyre import geometry

    # the chart
    chart = geometry.SphereLonLat()

    # the polygon through a list of (longitude, latitude) corners, walked as given
    def polygon(corners):
        """
        The polygon bound by the ring through {corners}
        """
        # place the corners
        points = [chart.point(longitude=x, latitude=y) for x, y in corners]
        # and make the polygon
        return geometry.SpherePolygon(rings=[geometry.SphereRing(vertices=points)])

    # a footprint of two pieces, on either side of the antimeridian
    footprint = geometry.union(
        shapes=[
            polygon(((176, 0), (180, 0), (180, 4), (176, 4))),
            polygon(((-180, 0), (-176, 0), (-176, 4), (-180, 4))),
        ]
    )
    # has both pieces
    assert len(footprint) == 2

    # a point in the second piece
    point = chart.point(longitude=-178, latitude=2)
    # is in the footprint, whichever is asked first
    assert geometry.intersects(a=footprint, b=point)
    # in either order
    assert geometry.intersects(a=point, b=footprint)
    # and as a method of the footprint
    assert footprint.intersects(other=point)

    # a box around the antimeridian
    box = geometry.SphereBox(west=179, south=1, east=-179, north=3)
    # meets the footprint
    assert geometry.intersects(a=box, b=footprint)
    # and as a method of the box
    assert box.intersects(other=footprint)
    # but a box far away doesn't
    assert not geometry.intersects(
        a=geometry.SphereBox(west=0, south=0, east=10, north=10), b=footprint
    )

    # a path that crosses the footprint
    path = geometry.SpherePath(
        vertices=[chart.point(longitude=170, latitude=2), chart.point(longitude=-170, latitude=2)]
    )
    # meets it
    assert geometry.intersects(a=footprint, b=path)
    # and as a method of the path
    assert path.intersects(other=footprint)

    # a polygon that overlaps one of the pieces
    region = polygon(((174, 1), (178, 1), (178, 3), (174, 3)))
    # meets the footprint
    assert geometry.intersects(a=region, b=footprint)
    # and as a method of the polygon
    assert region.intersects(other=footprint)

    # a polygon covers the points inside it
    assert geometry.covers(a=region, b=chart.point(longitude=176, latitude=2))
    # and so does a box
    assert box.covers(other=chart.point(longitude=180, latitude=2))

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
