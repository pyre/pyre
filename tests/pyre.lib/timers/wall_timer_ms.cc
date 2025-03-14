// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


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
using walltimer_t = pyre::timers::wall_timer_t;


// verify that we can manipulate the timer state
int
main()
{
    // make a timer
    walltimer_t timer("tests.timer");
    // and start it
    timer.start();

    // nap duration
    auto nap = 50ms;
    // go to sleep for a bit
    std::this_thread::sleep_for(nap);
    // stop it
    timer.stop();

    // make a channel
    pyre::journal::debug_t channel("pyre.timers");
    // activate it
    // channel.activate();
    // and show me
    channel << "elapsed time: " << timer.ms() << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
