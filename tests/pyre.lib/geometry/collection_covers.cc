// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check when a union of intervals covers an interval: its members may do it together, as long as
// they leave no gap, and intervals that touch at an end leave none; and check that a shape covers
// a union when it covers every member


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
    // pieces that overlap, then touch, in no particular order
    auto pieces = union_t {
        interval_t(point_t(3.0), point_t(5.0)),
        interval_t(point_t(0.0), point_t(2.0)),
        interval_t(point_t(1.0), point_t(3.0)),
    };
    // cover what they span together
    assert(pyre::geometry::covers(pieces, interval_t(point_t(0.0), point_t(5.0))));
    // and any part of it
    assert(pyre::geometry::covers(pieces, interval_t(point_t(1.5), point_t(4.0))));
    // but not past their ends
    assert(not pyre::geometry::covers(pieces, interval_t(point_t(-1.0), point_t(4.0))));
    assert(not pyre::geometry::covers(pieces, interval_t(point_t(1.0), point_t(6.0))));

    // pieces with a gap between them
    auto apart = union_t {
        interval_t(point_t(0.0), point_t(1.0)),
        interval_t(point_t(2.0), point_t(3.0)),
    };
    // don't cover an interval across the gap
    assert(not pyre::geometry::covers(apart, interval_t(point_t(0.5), point_t(2.5))));
    // but do cover one on either side of it
    assert(pyre::geometry::covers(apart, interval_t(point_t(2.0), point_t(2.5))));
    // and every union covers the empty interval
    assert(pyre::geometry::covers(union_t(), interval_t()));

    // an interval covers a union when it covers every member
    assert(pyre::geometry::covers(interval_t(point_t(0.0), point_t(3.0)), apart));
    assert(not pyre::geometry::covers(interval_t(point_t(0.0), point_t(2.5)), apart));
    // and a union covers another when it covers every member of the other
    assert(pyre::geometry::covers(pieces, apart));
    assert(not pyre::geometry::covers(apart, pieces));

    // all done
    return 0;
}


// end of file
