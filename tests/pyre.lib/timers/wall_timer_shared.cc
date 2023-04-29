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
using walltimer_t = pyre::timers::wall_timer_t;


// verify that two timers that have the same name share the same movement
int main() {
    // make a timer
    walltimer_t t1("tests.timer");
    // start it
    t1.start();
    // it should now be active
    assert (t1.active() == true);

    // nap duration
    auto nap = 50ms;
    // go to sleep for a bit
    std::this_thread::sleep_for(nap);

    // make another timer with the same name
    walltimer_t t2("tests.timer");
    // verify it is running
    assert (t2.active() == true);
    // stop it
    t2.stop();

    // verify we stopped both timers
    assert (t1.active() == false);
    assert (t2.active() == false);
    // and that they both show the same accumulated time
    assert (t1.read() == t2.read());

    // all done
    return 0;
}


// end of file
