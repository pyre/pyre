// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that the points of a product space are pairs of points of its factors, and that its
// dimension is the sum of theirs


// portability
#include <portinfo>
// STL
#include <cassert>
#include <sstream>
// support
#include <pyre/geometry.h>


// type aliases
using surface_t = pyre::geometry::ellipsoid_t;
using height_t = pyre::geometry::euclidean_t<1>;
using space_t = pyre::geometry::product_t<surface_t, height_t>;
using point_t = pyre::geometry::point_t<space_t>;


// driver
int
main()
{
    // the space of positions above the ellipsoid
    auto space = space_t(surface_t::wgs84(), height_t());
    // has three dimensions
    static_assert(space_t::dimension() == 3);
    // and remembers its factors
    assert(space.first() == surface_t::wgs84());

    // a point on the equator, a hundred meters up
    auto p = point_t(
        pyre::geometry::point_t<surface_t>(1.0, 0.0, 0.0),
        pyre::geometry::point_t<height_t>(100.0));
    // has its parts
    assert(p.data().first == pyre::geometry::point_t<surface_t>(1.0, 0.0, 0.0));
    assert(p.data().second[0] == 100.0);

    // and is written as its two parts
    auto stream = std::ostringstream();
    stream << p;
    assert(stream.str() == "(1, 0, 0), (100)");

    // all done
    return 0;
}


// end of file
