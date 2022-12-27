// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_api_h)
#define pyre_timers_api_h


// package api
namespace pyre::timers {
    // wall clock timer
    using wall_timer_t = Timer<WallClock, Proxy>;
    // process CPU time
    using process_timer_t = Timer<ProcessClock, Proxy>;
}


#endif

// end of file
