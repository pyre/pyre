// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// get the timers
#include <pyre/timers.h>
// support
#include <cassert>


// type aliases
using walltimer_t = pyre::timers::wall_timer_t;


// compile time sanity check: make sure the header file is accessible
int
main()
{
    // make a timer
    walltimer_t timer("tests.timer");
    // make sure it knows its name
    assert(timer.name() == "tests.timer");
    // and it starts out inactive
    assert(timer.active() == false);

    // nothing to do
    return 0;
}


// end of file
