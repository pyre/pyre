// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// verify that we can instantiate and manipulate inventories


// get the timers
#include <pyre/timers.h>
// and the journal
#include <pyre/journal.h>

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

    // make a channel
    pyre::journal::debug_t channel("pyre.timers");
    // activate it
    // channel.activate();
    // and show me
    channel
        // show me the sum
        << "sum: " << sum << pyre::journal::newline
        // show me the elapsed time
        << "elapsed time: " << timer.ms()
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
