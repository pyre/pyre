// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check when a path meets other shapes: a polygon it crosses or lies in, another path, a box, and
// a point on it


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
using box_t = pyre::geometry::box_t<chart_t>;
using path_t = pyre::geometry::path_t<chart_t>;
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

    // a square
    auto square = polygon_t({ ring_t({ at(0, 0), at(10, 0), at(10, 10), at(0, 10) }) });

    // a path across it
    auto across = path_t({ at(-5, 5), at(15, 5) });
    // meets it, whichever is asked first
    assert(pyre::geometry::intersects(square, across));
    assert(pyre::geometry::intersects(across, square));
    // a path inside it
    assert(pyre::geometry::intersects(square, path_t({ at(2, 2), at(4, 4) })));
    // but not a path that goes around it
    assert(not pyre::geometry::intersects(square, path_t({ at(-5, -5), at(15, -5), at(15, 15) })));

    // a path that crosses the first one
    assert(pyre::geometry::intersects(across, path_t({ at(5, 0), at(5, 10) })));
    // and one that doesn't
    assert(not pyre::geometry::intersects(across, path_t({ at(20, 0), at(20, 10) })));

    // a box the path runs through
    assert(pyre::geometry::intersects(across, box_t(12, 0, 20, 10)));
    // and one it misses
    assert(not pyre::geometry::intersects(across, box_t(20, 0, 30, 10)));

    // a path along the equator, which is a great circle
    auto equator = path_t({ at(-5, 0), at(15, 0) });
    // holds the points of the equator between its ends
    assert(pyre::geometry::intersects(equator, at(5, 0)));
    // but not the points of the parallel through the ends of {across}, since its geodesic edge
    // bulges north of that parallel
    assert(not pyre::geometry::intersects(across, at(5, 5)));

    // all done
    return 0;
}


// end of file
