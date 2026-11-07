// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check when two polygons share a point: when their boundaries cross or only touch, when one
// holds the other, across the antimeridian, and never when one lies in a hole of the other


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
using ring_t = pyre::geometry::ring_t<chart_t>;
using polygon_t = pyre::geometry::polygon_t<chart_t>;


// driver
int
main()
{
    // the chart
    auto chart = chart_t();
    // the point at a longitude and a latitude
    auto at = [&chart](double longitude, double latitude) {
        // place it
        return chart.point({ longitude, latitude });
    };
    // a square, walked counterclockwise, from its southwest corner and its size, in degrees
    auto square = [&at](double west, double south, double size) {
        // the ring through its corners
        return ring_t(
            { at(west, south), at(west + size, south), at(west + size, south + size),
              at(west, south + size) });
    };

    // two squares that overlap
    auto a = polygon_t({ square(0, 0, 10) });
    auto b = polygon_t({ square(5, 5, 10) });
    // share a point
    assert(pyre::geometry::intersects(a, b));
    // whichever is asked first
    assert(pyre::geometry::intersects(b, a));

    // a square inside another one, with no boundaries in common
    auto inner = polygon_t({ square(2, 2, 2) });
    // shares its points with it
    assert(pyre::geometry::intersects(a, inner));
    assert(pyre::geometry::intersects(inner, a));

    // a square far away
    auto far = polygon_t({ square(100, 40, 5) });
    // shares nothing
    assert(not pyre::geometry::intersects(a, far));

    // two squares that overlap across the antimeridian
    auto east = polygon_t({ square(176, 0, 6) });
    auto west = polygon_t({ square(-180, 2, 6) });
    // share a point
    assert(pyre::geometry::intersects(east, west));
    // and two that share only an edge, along the meridian at 182 degrees east
    auto beside = polygon_t({ square(-178, 2, 6) });
    // touch, which counts, since the polygons are closed
    assert(pyre::geometry::intersects(east, beside));

    // a square with a square hole, walked clockwise so that the region to its left is everything
    // outside of it
    auto frame = polygon_t({ square(0, 0, 10), square(3, 3, 4).reversed() });
    // doesn't hold the points of the hole
    assert(not frame.contains(at(5, 5)));
    // and shares nothing with a polygon inside the hole
    assert(not pyre::geometry::intersects(frame, polygon_t({ square(4, 4, 2) })));
    // but does with one that reaches out of it
    assert(pyre::geometry::intersects(frame, polygon_t({ square(4, 4, 5) })));

    // the polygon without rings is the whole sphere, which meets everything
    assert(pyre::geometry::intersects(polygon_t({}), far));

    // all done
    return 0;
}


// end of file
