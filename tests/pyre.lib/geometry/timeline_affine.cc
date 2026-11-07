// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that instants subtract to give durations, that durations move instants, and that the
// civil calendar maps times to instants and back


// portability
#include <portinfo>
// STL
#include <cassert>
#include <chrono>
// support
#include <pyre/geometry.h>


// type aliases
using space_t = pyre::geometry::timeline_t;
using point_t = pyre::geometry::point_t<space_t>;
using duration_t = space_t::vector_type;
using calendar_t = space_t::time_type;


// driver
int
main()
{
    // the epoch of the timeline: the start of 2025-10-14
    auto epoch = calendar_t(std::chrono::sys_days(std::chrono::year(2025) / 10 / 14));
    // the timeline
    auto timeline = space_t(epoch);

    // the instant at the epoch is the origin
    assert(timeline.point(epoch).data() == 0);
    // an hour later
    auto later = timeline.point(epoch + std::chrono::hours(1));
    // is 3600 seconds after the origin
    assert(later.data() == 3600);
    // and the calendar recovers its time
    assert(timeline.time(later) == epoch + std::chrono::hours(1));

    // the two instants are an hour apart
    auto origin = timeline.point(epoch);
    assert(later - origin == duration_t(3600));
    assert(timeline.distance(origin, later) == 3600);
    // and moving the origin by an hour lands on the later one
    assert(origin + duration_t(3600) == later);

    // all done
    return 0;
}


// end of file
