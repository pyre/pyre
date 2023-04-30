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
    auto mark = timer.start();

    // do something
    [[maybe_unused]] double sum = 0;
    for (int i = 0; i < 1000 * 1000; ++i) {
        sum += i;
    }

    // stop it
    auto elapsed = timer.stop();
    // verify the elapsed time is greater than zero
    assert(mark + elapsed >= mark);

    // all done
    return 0;
}


// end of file
