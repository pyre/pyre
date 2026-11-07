// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a brick counts its own corners, even when its space has more dimensions than it
// does, and that it places a point along every axis of that space


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using point_t = pyre::geometry::point_t<pyre::geometry::euclidean_t<3>>;
using brick_t = pyre::geometry::brick_t<2, point_t>;


// driver
int
main()
{
    // a unit square in the plane z = 1
    auto square = brick_t(
        point_t(0.0, 0.0, 1.0), point_t(1.0, 0.0, 1.0), point_t(1.0, 1.0, 1.0),
        point_t(0.0, 1.0, 1.0));

    // lives in three dimensions
    static_assert(brick_t::dimension() == 3);
    // but is two dimensional
    static_assert(brick_t::intrinsicDimension() == 2);
    // so it has four corners
    static_assert(brick_t::size() == 4);

    // a point above the square
    auto flags = square.interior(point_t(0.5, 0.5, 2.0));
    // is within its span in the plane, and above it along the third axis
    assert(flags[0] == 0);
    assert(flags[1] == 0);
    assert(flags[2] == 1);

    // all done
    return 0;
}


// end of file
