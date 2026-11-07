// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the region a ring bounds: the region to its left, which for a ring walked
// counterclockwise is the small region inside it and for the same ring walked clockwise is the
// rest of the sphere; the points on the ring; a ring around a pole; and the orientation that
// makes a ring bound the smaller of its two regions


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
#include <numbers>
#include <vector>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
using point_t = pyre::geometry::point_t<pyre::geometry::sphere_t>;
using ring_t = pyre::geometry::ring_t<chart_t>;


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

    // a small square walked counterclockwise, with its inside to the left
    auto square = ring_t({ at(0, 0), at(10, 0), at(10, 10), at(0, 10) });
    // holds its center
    assert(square.contains(at(5, 5)));
    // and the points on it
    assert(square.contains(at(10, 5)));
    assert(square.boundary(at(10, 5)));
    // but not the rest of the earth
    assert(not square.contains(at(20, 5)));
    assert(not square.contains(at(185, -5)));
    // and its area is small
    assert(square.area() < 0.1);

    // the same square walked clockwise
    auto outside = square.reversed();
    // bounds the rest of the earth
    assert(not outside.contains(at(5, 5)));
    assert(outside.contains(at(20, 5)));
    assert(outside.contains(at(185, -5)));
    // still holds the points on the ring
    assert(outside.contains(at(10, 5)));
    // and the two areas add up to the whole sphere
    assert(std::abs(square.area() + outside.area() - 4 * std::numbers::pi) < 1e-9);

    // orienting either one makes it bound the small square
    assert(pyre::geometry::orient(square) == square);
    assert(pyre::geometry::orient(outside) == square);

    // a ring of geodesic edges around the north pole, walked counterclockwise
    auto cap = ring_t({ at(0, 80), at(90, 80), at(180, 80), at(270, 80) });
    // holds the pole
    assert(cap.contains(point_t(pyre::geometry::spherical::north)));
    // and the points near it on every side of the antimeridian
    assert(cap.contains(at(179, 85)));
    assert(cap.contains(at(-179, 85)));
    // but not the south pole
    assert(not cap.contains(point_t(pyre::geometry::spherical::south)));

    // all done
    return 0;
}


// end of file
