// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that the distance on a sphere is the length of the shorter great circle arc, for points a
// quarter turn apart, antipodal points, and points very close together


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
#include <numbers>
// support
#include <pyre/geometry.h>


// type aliases
using space_t = pyre::geometry::sphere_t;
using point_t = pyre::geometry::point_t<space_t>;


// driver
int
main()
{
    // a sphere with the mean radius of the earth, in meters
    auto space = space_t(6371008.8);
    // the length of a quarter of one of its great circles
    auto quarter = space.radius() * std::numbers::pi / 2;

    // a point on the equator, a point on the equator a quarter turn east of it, and the north pole
    auto p = point_t(1.0, 0.0, 0.0);
    auto q = point_t(0.0, 1.0, 0.0);
    auto north = point_t(0.0, 0.0, 1.0);
    // and the point opposite to {p}
    auto antipode = point_t(-1.0, 0.0, 0.0);

    // points a quarter turn apart are a quarter of a great circle apart
    assert(std::abs(space.distance(p, q) - quarter) < 1e-6);
    assert(std::abs(space.distance(p, north) - quarter) < 1e-6);
    // antipodal points are half a great circle apart
    assert(std::abs(space.distance(p, antipode) - 2 * quarter) < 1e-6);

    // a point a micro-radian away from {p} along the equator
    auto near = point_t(std::cos(1e-6), std::sin(1e-6), 0.0);
    // is a micro-radian of arc away, to within a fraction of a millimeter
    assert(std::abs(space.distance(p, near) - space.radius() * 1e-6) < 1e-4);

    // all done
    return 0;
}


// end of file
