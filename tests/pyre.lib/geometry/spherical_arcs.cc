// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the arcs of great circles: which points are on them, which pairs cross, which only
// touch, and that two arcs whose circles meet across the sphere from both of them don't cross


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
// alias the namespace
namespace spherical = pyre::geometry::spherical;


// driver
int
main()
{
    // the chart
    auto chart = chart_t();
    // the unit vector at a longitude and a latitude
    auto at = [&chart](double longitude, double latitude) {
        // place the point and hand off its vector
        return chart.point({ longitude, latitude }).data();
    };

    // an arc along the equator, from 0 to 40 degrees east
    auto a = at(0, 0);
    auto b = at(40, 0);
    // holds its ends
    assert(spherical::onArc(a, b, a));
    assert(spherical::onArc(a, b, b));
    // and the points between them
    assert(spherical::onArc(a, b, at(20, 0)));
    // but not the rest of the equator
    assert(not spherical::onArc(a, b, at(60, 0)));
    // nor the points across the sphere from it
    assert(not spherical::onArc(a, b, at(200, 0)));

    // an arc along the meridian at 20 degrees east, across the equator
    auto c = at(20, -10);
    auto d = at(20, 10);
    // crosses the first one
    assert(spherical::crosses(a, b, c, d));
    // in either order
    assert(spherical::crosses(c, d, a, b));
    // and the two meet
    assert(spherical::meets(a, b, c, d));

    // an arc that ends on the first one
    auto e = at(30, 10);
    auto f = at(30, 0);
    // doesn't cross it
    assert(not spherical::crosses(a, b, e, f));
    // but meets it
    assert(spherical::meets(a, b, e, f));

    // an arc on the other side of the sphere, across the circle of the first one
    auto g = at(200, -10);
    auto h = at(200, 10);
    // straddles the circle of the first arc, but the circles meet across the sphere from it
    assert(not spherical::crosses(a, b, g, h));
    // so the two don't meet
    assert(not spherical::meets(a, b, g, h));

    // the highest point of an arc between two points at 60 degrees north, 90 degrees apart in
    // longitude, is north of both, since the great circle bulges toward the pole
    auto highest = spherical::highest(at(0, 60), at(90, 60)) * 180 / M_PI;
    assert(highest > 65);
    // and its lowest point is at its ends
    auto lowest = spherical::lowest(at(0, 60), at(90, 60)) * 180 / M_PI;
    assert(std::abs(lowest - 60) < 1e-9);

    // all done
    return 0;
}


// end of file
