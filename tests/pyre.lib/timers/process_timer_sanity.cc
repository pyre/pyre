// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the timers
#include <pyre/timers.h>
// support
#include <cassert>


// type aliases
using proctimer_t = pyre::timers::process_timer_t;


// compile time sanity check: make sure the header file is accessible
int main() {
    // make a timer
    proctimer_t timer("tests.timer");
    // make sure it knows its name
    assert (timer.name() == "tests.timer");
    // and it starts out inactive
    assert (timer.active() == false);

    // nothing to do
    return 0;
}


// end of file
