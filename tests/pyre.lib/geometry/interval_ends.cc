// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the ends of intervals: closed ends belong to the interval, ends at the infinities leave it
// unbounded, and an interval with its ends out of order is the empty one


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


// driver
int
main()
{
    // an interval
    auto interval = interval_t(point_t(1.0), point_t(2.0));
    // holds its ends
    assert(interval.contains(point_t(1.0)));
    assert(interval.contains(point_t(2.0)));
    // and the points between them
    assert(interval.contains(point_t(1.5)));
    // but nothing outside
    assert(not interval.contains(point_t(0.5)));
    assert(not interval.contains(point_t(2.5)));
    // it is bounded on both sides
    assert(interval.boundedBelow() and interval.boundedAbove());
    // and it isn't empty
    assert(not interval.empty());

    // an interval that is a single point
    auto single = interval_t(point_t(1.0), point_t(1.0));
    // holds that point
    assert(single.contains(point_t(1.0)));
    // and so it isn't empty
    assert(not single.empty());

    // an interval with its ends out of order
    auto backwards = interval_t(point_t(2.0), point_t(1.0));
    // is empty
    assert(backwards.empty());
    // holds nothing
    assert(not backwards.contains(point_t(1.5)));
    // and is the same as the empty interval
    assert(backwards == interval_t());

    // the rays
    auto from = interval_t::from(point_t(1.0));
    auto until = interval_t::until(point_t(1.0));
    // are bounded on one side only
    assert(from.boundedBelow() and not from.boundedAbove());
    assert(until.boundedAbove() and not until.boundedBelow());
    // and reach as far as one can go on the other
    assert(from.contains(point_t(1.0e300)));
    assert(until.contains(point_t(-1.0e300)));

    // the whole line
    auto line = interval_t::line();
    // is bounded on neither side
    assert(not line.boundedBelow() and not line.boundedAbove());
    // and holds every point
    assert(line.contains(point_t(0.0)));

    // all done
    return 0;
}


// end of file
