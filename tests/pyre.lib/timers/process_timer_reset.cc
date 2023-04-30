// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// verify that we can instantiate and manipulate inventories


// get the timers
#include <pyre/timers.h>

// support
#include <thread>
#include <cassert>
// access the {chrono} literals
using namespace std::literals;

// convenience
using proctimer_t = pyre::timers::process_timer_t;


// verify that we can manipulate the timer state
int
main()
{
    // make a timer
    proctimer_t timer("tests.timer");
    // and start it
    timer.start();
    // stop it
    timer.stop();

    // reset it
    timer.reset();
    // verify it is inactive
    assert(timer.active() == false);
    // and that the accumulated time is reset to zero
    assert(timer.read() == proctimer_t::duration_type::zero());

    // all done
    return 0;
}


// end of file
