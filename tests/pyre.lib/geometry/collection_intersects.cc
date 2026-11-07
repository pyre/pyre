// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check when a union of intervals shares a point with a shape: when one of its members does; the
// pair that knows how is the union and the shape, and the relation answers in either order


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
    // the two acquisitions of a pair, which lie apart
    auto pair = union_t {
        interval_t(point_t(0.0), point_t(1.0)),
        interval_t(point_t(10.0), point_t(11.0)),
    };

    // a window around the first one meets the pair
    assert(pyre::geometry::intersects(pair, interval_t(point_t(0.5), point_t(2.0))));
    // and so does one around the second
    assert(pyre::geometry::intersects(pair, interval_t(point_t(10.5), point_t(12.0))));
    // but a window in the gap between them does not
    assert(not pyre::geometry::intersects(pair, interval_t(point_t(2.0), point_t(9.0))));

    // the relation answers with the interval first, too
    assert(pyre::geometry::intersects(interval_t(point_t(0.5), point_t(2.0)), pair));
    assert(not pyre::geometry::intersects(interval_t(point_t(2.0), point_t(9.0)), pair));

    // two unions meet when a member of one meets a member of the other
    assert(pyre::geometry::intersects(pair, union_t { interval_t(point_t(5.0), point_t(10.0)) }));
    // and not otherwise
    assert(
        not pyre::geometry::intersects(pair, union_t { interval_t(point_t(5.0), point_t(6.0)) }));

    // the empty union meets nothing
    assert(not pyre::geometry::intersects(union_t(), interval_t::line()));

    // all done
    return 0;
}


// end of file
