// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved


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
int main() {
    // make a timer
    proctimer_t timer("tests.timer");
    // and start it
    timer.start();

    // do something
    double sum=0;
    for (int i=0; i < 1000*1000; ++i) {
        sum += i;
    }

    // stop it
    timer.stop();

    // reset the timer
    timer.reset();
    // verify it is inactive
    assert (timer.active() == false);
    // and that the accumulated time is reset to zero
    assert (timer.read() == proctimer_t::duration_type::zero());

    // all done
    return 0;
}


// end of file
