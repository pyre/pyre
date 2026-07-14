// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// clock that measures the passage of real time
// the current implementation is a trivial wrapper over {std::chrono::steady_clock}
class pyre::timers::WallClock {
    // types
public:
    using string_type = std::string;
    using clock_type = std::chrono::steady_clock;
    using duration_type = clock_type::duration;
    using time_point_type = clock_type::time_point;

    // interface
public:
    inline static auto type() -> string_type;
    inline static auto now() -> time_point_type;
};


// get the inline definitions
#include "WallClock.icc"


// end of file
