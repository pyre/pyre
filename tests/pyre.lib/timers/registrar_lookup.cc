// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the timers
#include <pyre/timers.h>
// support
#include <cassert>


// type aliases
using movement_t = pyre::timers::movement_t<pyre::timers::wall_clock_t>;
using registrar_t = pyre::timers::registrar_t<movement_t>;


// exercise the timer state index
int main() {
    // make an index
    registrar_t registrar;

    // lookup a name
    auto & movement = registrar.lookup("test.registrar");
    // make sure its activation state is what we expect
    assert(movement.active() == false);

    // all done
    return 0;
}


// end of file
