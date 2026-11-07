// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that points in euclidean space subtract to give vectors, and that translating a point by
// the vector from another one lands on it


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using space_t = pyre::geometry::euclidean_t<2>;
using point_t = pyre::geometry::point_t<space_t>;
using vector_t = space_t::vector_type;


// driver
int
main()
{
    // a pair of points
    auto p = point_t(1.0, 2.0);
    auto q = point_t(4.0, -1.0);

    // the vector from {p} to {q}
    auto v = q - p;
    // has the change of each coordinate as its components
    assert((v == vector_t { 3.0, -3.0 }));
    // translating {p} by it lands on {q}
    assert(p + v == q);
    // and translating {q} back lands on {p}
    assert(q - v == p);

    // all done
    return 0;
}


// end of file
