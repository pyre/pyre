// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that equal intervals hash alike, and that an interval and the one with its ends swapped
// hash differently


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
    // hashes like another made the same way
    assert(interval.hash() == interval_t(point_t(1.0), point_t(2.0)).hash());
    // the one with its ends swapped is a different interval
    assert(interval != interval_t(point_t(2.0), point_t(1.0)));
    // with a different hash
    assert(interval.hash() != interval_t(point_t(2.0), point_t(1.0)).hash());
    // and the whole line hashes like itself
    assert(interval_t::line().hash() == interval_t::line().hash());

    // all done
    return 0;
}


// end of file
