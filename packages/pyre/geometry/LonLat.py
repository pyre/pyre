# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the bindings
from .. import libpyre


# the longitude-latitude chart of the sphere
class LonLat:
    """
    The longitude-latitude chart of the sphere, in degrees, which names the points of the sphere
    and builds the shapes through them

    Every method that takes a point or a box takes keywords, so the order of the coordinates
    never shows; sequences of vertices are (longitude, latitude) pairs, longitude first, the order
    of WKB, GeoJSON, PostGIS and the common metadata repository

    A ring bounds the region to its left, as one walks it from vertex to vertex seen from outside
    the sphere: counterclockwise around what it encloses. A ring walked the other way bounds the
    complement, nearly the whole sphere for a small ring. Data whose convention is known should be
    read with it, and reversed when it disagrees; rings drawn or typed by people, which come in
    either direction, should go through {pyre.geometry.orient}, which walks a ring so that it
    bounds the smaller of its two regions. The section on regions on the sphere in
    doc/design/geometry.md explains why
    """

    # interface
    def point(self, *, longitude: float, latitude: float):
        """
        The point at {longitude} and {latitude}, in degrees
        """
        # ask the chart
        return self.chart.point(longitude=longitude, latitude=latitude)

    def coordinates(self, point) -> tuple[float, float]:
        """
        The longitude and latitude of {point}, in degrees, in that order
        """
        # ask the chart
        return self.chart.coordinates(point=point)

    def box(self, *, west: float, south: float, east: float, north: float):
        """
        The points from the meridian at {west} east to the one at {east}, and from the parallel at
        {south} to the one at {north}, in degrees; a box whose west edge is east of its east edge
        straddles the antimeridian
        """
        # make one
        return libpyre.geometry.SphereBox(west=west, south=south, east=east, north=north)

    def path(self, *, vertices, geodesic: bool = True):
        """
        The path through {vertices}, (longitude, latitude) pairs in degrees, with edges that are
        great-circle arcs when {geodesic} is true, and straight in this chart otherwise
        """
        # make one
        return libpyre.geometry.SpherePath(
            vertices=self.points(vertices=vertices), geodesic=geodesic
        )

    def ring(self, *, vertices, geodesic: bool = True):
        """
        The ring through {vertices}, (longitude, latitude) pairs in degrees, which bounds the
        region to its left; its edges are great-circle arcs when {geodesic} is true, and straight
        in this chart otherwise; the ring closes itself, so its last vertex need not repeat its
        first
        """
        # make one
        return libpyre.geometry.SphereRing(
            vertices=self.points(vertices=vertices), geodesic=geodesic
        )

    def polygon(self, *, rings, geodesic: bool = True):
        """
        The points in the regions bound by all of the {rings}, each a sequence of (longitude,
        latitude) pairs in degrees: the first one counterclockwise around the polygon, the others
        clockwise around its holes; the edges are great-circle arcs when {geodesic} is true, and
        straight in this chart otherwise
        """
        # make the rings
        rings = [self.ring(vertices=ring, geodesic=geodesic) for ring in rings]
        # and the polygon they bound
        return libpyre.geometry.SpherePolygon(rings=rings)

    # implementation details
    def points(self, *, vertices) -> list:
        """
        The points at the given {vertices}, (longitude, latitude) pairs in degrees
        """
        # place each one
        return [
            self.point(longitude=longitude, latitude=latitude) for longitude, latitude in vertices
        ]

    # metamethods
    def __init__(self, **kwds):
        """
        Make the chart
        """
        # chain up
        super().__init__(**kwds)
        # the chart of the bindings
        self.chart = libpyre.geometry.SphereLonLat()
        # all done
        return


# end of file
