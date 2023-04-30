// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the timers
#include <pyre/timers.h>
#include <pyre/journal.h>
// support
#include <thread>
#include <cassert>
// access the {chrono} literals
using namespace std::literals;


// type aliases
using proctimer_t = pyre::timers::process_timer_t;


// verify that two timers that have the same name share the same movement
int main() {
    // make a timer
    proctimer_t t("tests.timer");
    // start it
    t.start();

    // do something
    double sum=0;
    for (int i=0; i < 1000*1000; ++i) {
        sum += i;
    }

    // stop the timer
    t.stop();

    // make a channel
    pyre::journal::debug_t channel("tests.timer");
    // activate it
    // channel.activate();
    // show me
    channel
        // show me the sum
        << "sum: " << sum << pyre::journal::newline
        // show me the elapsed time
        << "elapsed time: " << t.us()
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
