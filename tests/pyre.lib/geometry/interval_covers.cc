// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check when one interval covers another: when it holds every point of the other, ends included;
// the relation runs one way only, and every interval covers the empty one


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
    auto outer = interval_t(point_t(0.0), point_t(10.0));
    // covers the ones inside it
    assert(pyre::geometry::covers(outer, interval_t(point_t(2.0), point_t(3.0))));
    // including the ones that share its ends
    assert(pyre::geometry::covers(outer, interval_t(point_t(0.0), point_t(10.0))));
    // but not the ones that stick out
    assert(not pyre::geometry::covers(outer, interval_t(point_t(5.0), point_t(11.0))));
    // and not the other way around
    assert(not pyre::geometry::covers(interval_t(point_t(2.0), point_t(3.0)), outer));

    // every interval covers the empty one
    assert(pyre::geometry::covers(outer, interval_t()));
    // even the empty one
    assert(pyre::geometry::covers(interval_t(), interval_t()));
    // which covers nothing else
    assert(not pyre::geometry::covers(interval_t(), outer));

    // a ray covers the intervals on its side
    assert(pyre::geometry::covers(interval_t::from(point_t(0.0)), outer));
    // but not the ones that reach past its end
    assert(not pyre::geometry::covers(interval_t::until(point_t(5.0)), outer));

    // all done
    return 0;
}


// end of file
