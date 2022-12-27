// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the timers
#include <pyre/timers.h>
// support
#include <thread>
#include <cassert>
// access the {chrono} literals
using namespace std::literals;


// type aliases
using proctimer_t = pyre::timers::process_timer_t;


// verify that two timers that have the same name share the same movement
int
main()
{
    // make a timer
    proctimer_t t1("tests.timer");
    // start it
    t1.start();
    // it should now be active
    assert(t1.active() == true);

    // do something
    [[maybe_unused]] double sum = 0;
    for (int i = 0; i < 1000 * 1000; ++i) {
        sum += i;
    }

    // make another timer with the same name
    proctimer_t t2("tests.timer");
    // verify it is running
    assert(t2.active() == true);
    // stop it
    t2.stop();

    // verify we stopped both timers
    assert(t1.active() == false);
    assert(t2.active() == false);
    // and that they both show the same accumulated time
    assert(t1.read() == t2.read());

    // all done
    return 0;
}


// end of file
