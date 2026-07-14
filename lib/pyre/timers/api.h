// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// package api
namespace pyre::timers {
    // wall clock timer
    using wall_timer_t = Timer<WallClock, Proxy>;
    // process CPU time
    using process_timer_t = Timer<ProcessClock, Proxy>;
} // namespace pyre::timers


// end of file
