// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the hull of two intervals, the smallest interval that holds both, and the envelope of a
// union of intervals, which is the hull of its members


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using line_t = pyre::geometry::euclidean_t<1>;
using point_t = pyre::geometry::point_t<line_t>;
using interval_t = pyre::geometry::interval_t<line_t>;
using union_t = pyre::geometry::collection_t<interval_t>;


// driver
int
main()
{
    // two intervals that lie apart
    auto left = interval_t(point_t(0.0), point_t(1.0));
    auto right = interval_t(point_t(3.0), point_t(4.0));
    // have a hull that spans the gap between them
    assert(pyre::geometry::hull(left, right) == interval_t(point_t(0.0), point_t(4.0)));
    // in either order
    assert(pyre::geometry::hull(right, left) == interval_t(point_t(0.0), point_t(4.0)));
    // an interval inside another adds nothing to it
    assert(
        pyre::geometry::hull(interval_t(point_t(-1.0), point_t(5.0)), left)
        == interval_t(point_t(-1.0), point_t(5.0)));
    // and neither does the empty interval
    assert(pyre::geometry::hull(left, interval_t()) == left);
    assert(pyre::geometry::hull(interval_t(), left) == left);
    // a ray keeps its unbounded side
    assert(not pyre::geometry::hull(left, interval_t::from(point_t(2.0))).boundedAbove());

    // the envelope of a union
    auto pieces = union_t { right, left, interval_t(point_t(2.0), point_t(2.5)) };
    // is the hull of its members
    assert(pieces.envelope() == interval_t(point_t(0.0), point_t(4.0)));
    // and the envelope of the empty union is the empty interval
    assert(union_t().envelope().empty());

    // all done
    return 0;
}


// end of file
