// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// clock that measures the amount of CPU time charged to this process
// the current implementation is a trivial wrapper over the POSIX {clock} support
class pyre::timers::ProcessClock {
    // types
public:
    using string_type = std::string;
    using duration_type = std::chrono::duration<long long int, std::nano>;
    using time_point_type = std::chrono::time_point<ProcessClock, duration_type>;

    // interface
public:
    inline static auto type() -> string_type;
    inline static auto now() -> time_point_type;
};


// get the inline definitions
#include "ProcessClock.icc"


// end of file
