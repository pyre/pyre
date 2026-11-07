// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check when a box shares a point with another box, across the antimeridian too, and with a
// polygon, including the boxes that go all the way around and reach a pole


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
using box_t = pyre::geometry::box_t<chart_t>;
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

    // two boxes that overlap across the antimeridian
    assert(pyre::geometry::intersects(box_t(170, 0, -170, 10), box_t(-175, 5, -160, 15)));
    // two that don't, though their longitudes overlap
    assert(not pyre::geometry::intersects(box_t(170, 0, -170, 10), box_t(175, 20, -175, 30)));
    // and the empty box, which meets nothing
    assert(not pyre::geometry::intersects(box_t(), box_t::sphere()));

    // a square polygon
    auto square = polygon_t({ ring_t({ at(0, 0), at(10, 0), at(10, 10), at(0, 10) }) });
    // meets a box that overlaps it
    assert(pyre::geometry::intersects(square, box_t(5, 5, 15, 15)));
    // and one inside it
    assert(pyre::geometry::intersects(box_t(2, 2, 3, 3), square));
    // and one around it
    assert(pyre::geometry::intersects(square, box_t(-20, -20, 20, 20)));
    // but not one beside it
    assert(not pyre::geometry::intersects(square, box_t(20, 0, 30, 10)));

    // the cap of the earth north of 80 degrees, a box that goes all the way around
    auto arctic = box_t(-180, 80, 180, 90);
    // meets a polygon around the pole
    auto cap = polygon_t({ ring_t({ at(0, 85), at(90, 85), at(180, 85), at(270, 85) }) });
    assert(pyre::geometry::intersects(arctic, cap));
    // but not the square near the equator
    assert(not pyre::geometry::intersects(arctic, square));

    // all done
    return 0;
}


// end of file
