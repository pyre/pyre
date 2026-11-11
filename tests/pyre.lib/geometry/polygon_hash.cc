// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that equal polygons hash alike, and that a polygon with a hole hashes differently from
// the one without it


// portability
#include <portinfo>
// STL
#include <cassert>
#include <vector>
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
    // the boundary of a square, walked counterclockwise
    auto outer = ring_t({ at(0, 0), at(10, 0), at(10, 10), at(0, 10) });
    // and a hole in it, walked clockwise
    auto hole = ring_t({ at(4, 4), at(4, 6), at(6, 6), at(6, 4) });

    // a polygon bound by the square
    auto square = polygon_t({ outer });
    // hashes like another made the same way
    assert(square.hash() == polygon_t({ outer }).hash());
    // the square with the hole
    auto frame = polygon_t({ outer, hole });
    // is a different polygon
    assert(square != frame);
    // with a different hash
    assert(square.hash() != frame.hash());

    // all done
    return 0;
}


// end of file
