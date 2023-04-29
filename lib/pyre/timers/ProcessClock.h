// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_ProcessClock_h)
#define pyre_timers_ProcessClock_h


// clock that measures the amount of CPU time charged to this process
// the current implementation is a trivial wrapper over the POSIX {clock} support
class pyre::timers::ProcessClock {
    // types
public:
    using duration_type = std::chrono::duration<long long int, std::nano>;
    using time_point_type = std::chrono::time_point<ProcessClock, duration_type>;

    // interface
public:
    inline static auto now() -> time_point_type;
};


// get the inline definitions
#define pyre_timers_ProcessClock_icc
#include "ProcessClock.icc"
#undef pyre_timers_ProcessClock_icc


#endif

// end of file
