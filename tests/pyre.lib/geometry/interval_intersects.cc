// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check when two intervals of the timeline share a point: when they overlap, when they touch at
// an end, and when either is unbounded; never when they lie apart or when one of them is empty


// portability
#include <portinfo>
// STL
#include <cassert>
#include <chrono>
// support
#include <pyre/geometry.h>


// type aliases
using timeline_t = pyre::geometry::timeline_t;
using interval_t = pyre::geometry::interval_t<timeline_t>;
using calendar_t = timeline_t::time_type;


// driver
int
main()
{
    // a timeline whose epoch is that of the system clock
    auto timeline = timeline_t();
    // the start of a day
    auto day = calendar_t(std::chrono::sys_days(std::chrono::year(2025) / 10 / 14));
    // the instant at a number of hours into that day
    auto at = [&](int hours) {
        return timeline.point(day + std::chrono::hours(hours));
    };

    // the window from six in the morning to six in the evening
    auto window = interval_t(at(6), at(18));

    // an acquisition that straddles its start
    assert(pyre::geometry::intersects(window, interval_t(at(5), at(7))));
    // one inside it
    assert(pyre::geometry::intersects(window, interval_t(at(10), at(11))));
    // one that ends right as the window opens shares that instant
    assert(pyre::geometry::intersects(window, interval_t(at(4), at(6))));
    // one entirely before it does not
    assert(not pyre::geometry::intersects(window, interval_t(at(1), at(2))));
    // nor one entirely after it
    assert(not pyre::geometry::intersects(window, interval_t(at(19), at(20))));

    // a window open on its start reaches back to acquisitions long before its end
    assert(pyre::geometry::intersects(interval_t::until(at(18)), interval_t(at(-100), at(-99))));
    // the whole line meets everything but the empty interval
    assert(pyre::geometry::intersects(interval_t::line(), window));
    assert(not pyre::geometry::intersects(interval_t::line(), interval_t()));

    // the relation is symmetric
    assert(pyre::geometry::intersects(interval_t(at(5), at(7)), window));

    // all done
    return 0;
}


// end of file
