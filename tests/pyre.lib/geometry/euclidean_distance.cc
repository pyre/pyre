// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that the distance in euclidean space is the length of the straight segment


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
// support
#include <pyre/geometry.h>


// type aliases
using space_t = pyre::geometry::euclidean_t<3>;
using point_t = pyre::geometry::point_t<space_t>;


// driver
int
main()
{
    // the space
    auto space = space_t();
    // a pair of points
    auto p = point_t(1.0, 2.0, 3.0);
    auto q = point_t(4.0, 6.0, 3.0);

    // the distance between them is the hypotenuse of a 3-4-5 triangle
    assert(std::abs(space.distance(p, q) - 5.0) < 1e-15);
    // the distance is symmetric
    assert(space.distance(p, q) == space.distance(q, p));
    // and vanishes from a point to itself
    assert(space.distance(p, p) == 0);

    // all done
    return 0;
}


// end of file
