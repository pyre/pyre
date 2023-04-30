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
using movement_t = pyre::timers::movement_t<pyre::timers::wall_clock_t>;
using registrar_t = pyre::timers::registrar_t<movement_t>;


// exercise the timer state index
int main() {
    // make an index
    registrar_t registrar;

    // make a movement proxy by looking up a timer name
    movement_t & m1(registrar.lookup("test.registrar"));
    // start the movement
    m1.start();
    // it should now be active
    assert (m1.active() == true);

    // nap duration
    auto nap = 50ms;
    // go to sleep for a bit
    std::this_thread::sleep_for(nap);

    // make another proxy to the same movement
    movement_t & m2(registrar.lookup("test.registrar"));
    // verify it is running
    assert (m2.active() == true);
    // stop it
    m2.stop();

    // verify that the two timers are now stopped
    assert (m1.active() == false);
    assert (m2.active() == false);
    // and that they show the same accumulated time
    assert (m1.read() == m2.read());

    // all done
    return 0;
}


// end of file
