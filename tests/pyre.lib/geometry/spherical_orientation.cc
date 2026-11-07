// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the side of a great circle a point is on: to the left, to the right, or on it, including
// a point so close to the plane of the circle that double precision gets its side wrong; and check
// the order of three directions around a point


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// alias the namespace
namespace spherical = pyre::geometry::spherical;


// driver
int
main()
{
    // three points on the equator, a quarter turn apart
    auto a = spherical::vector_t { 1, 0, 0 };
    auto b = spherical::vector_t { 0, 1, 0 };
    auto c = spherical::vector_t { -1, 0, 0 };
    // walking east from {a} to {b}, the north pole is to the left
    assert(spherical::orientation(a, b, spherical::north) == 1);
    // and the south pole to the right
    assert(spherical::orientation(a, b, spherical::south) == -1);
    // and a third point on the equator is on the circle
    assert(spherical::orientation(a, b, c) == 0);

    // three vectors whose third is one unit off the sum of the other two, so they are nearly in
    // one plane; the products in their determinant are so large that double precision gets its
    // sign wrong, and only the second pass, in twice the precision, gets it right; the exact
    // value is about 2.8e19, and double precision gives about -5.4e19
    auto p = spherical::vector_t { 611546045163.0, 737882493546.0, 733760317690.0 };
    auto q = spherical::vector_t { 12919335799.0, 15634224229.0, 840865321397.0 };
    auto r = spherical::vector_t { 624465380962.0, 753516717775.0, 1574625639088.0 };
    // the third is to the left of the circle of the other two
    assert(spherical::orientation(p, q, r) == 1);
    // and walking the circle the other way puts it to the right
    assert(spherical::orientation(q, p, r) == -1);

    // around the north pole, the meridians at 0, 90 and 180 degrees east come in counterclockwise
    // order, seen from outside the sphere
    assert(spherical::ordered(a, b, c, spherical::north));
    // and in the opposite order they don't
    assert(not spherical::ordered(c, b, a, spherical::north));

    // all done
    return 0;
}


// end of file
