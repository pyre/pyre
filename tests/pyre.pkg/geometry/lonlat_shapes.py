#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the longitude-latitude chart names points by keywords, gives back their coordinates
longitude first, and builds boxes, paths and polygons from (longitude, latitude) pairs
"""

# support
import pyre


def test():
    """
    Build each kind of shape through the chart
    """
    # the chart
    chart = pyre.geometry.lonlat()

    # a point, named by keywords
    point = chart.point(latitude=34.2, longitude=-118.2)
    # comes back longitude first
    longitude, latitude = chart.coordinates(point=point)
    # to within rounding
    assert abs(longitude + 118.2) < 1e-12
    # in both
    assert abs(latitude - 34.2) < 1e-12

    # a box, named by keywords
    box = chart.box(north=40, west=-120, south=30, east=-110)
    # keeps its edges
    assert (box.west, box.south, box.east, box.north) == (-120, 30, -110, 40)
    # and holds the point
    assert box.contains(point=point)

    # a path through (longitude, latitude) pairs, with edges straight in the chart
    path = chart.path(vertices=[(-120, 34.2), (-110, 34.2)], geodesic=False)
    # holds its vertices
    assert path.contains(point=chart.point(longitude=-110, latitude=34.2))
    # and runs through the box
    assert pyre.geometry.intersects(path, box)

    # a polygon from its corners, walked counterclockwise
    polygon = chart.polygon(rings=[[(-120, 30), (-110, 30), (-110, 40), (-120, 40)]])
    # holds the point
    assert polygon.contains(point=point)
    # and has a single ring
    assert len(polygon.rings) == 1

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
