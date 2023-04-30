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
    // take a timestamp
    auto zero = proctimer_t::clock_type::now();

    // do something
    [[maybe_unused]] double sum = 0;
    for (int i = 0; i < 1000 * 1000; ++i) {
        sum += i;
    }

    // make a timer
    proctimer_t timer("tests.timer");
    // and start it
    auto mark = timer.start();

    // verify it is now active
    assert(timer.active() == true);
    // and that its timestamp is later than our mark
    assert(mark > zero);

    // all done
    return 0;
}


// end of file
