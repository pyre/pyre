// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_WallClock_h)
#define pyre_timers_WallClock_h


// clock that measures the passage of real time
// the current implementation is a trivial wrapper over {std::chrono::steady_clock}
class pyre::timers::WallClock {
    // types
public:
    using clock_type = std::chrono::steady_clock;
    using duration_type = clock_type::duration;
    using time_point_type = clock_type::time_point;

    // interface
public:
    inline static auto now() -> time_point_type;
};


// get the inline definitions
#define pyre_timers_WallClock_icc
#include "WallClock.icc"
#undef pyre_timers_WallClock_icc


#endif

// end of file
