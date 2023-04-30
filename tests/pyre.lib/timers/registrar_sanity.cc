// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the timers
#include <pyre/timers.h>
// support
#include <cassert>


// type alias
using movement_t = pyre::timers::movement_t<pyre::timers::wall_clock_t>;
using registrar_t = pyre::timers::registrar_t<movement_t>;


// verify that the timer state index can be instantiated
int main() {
    // make an index
    registrar_t registrar;

    // make sure it's empty
    assert(registrar.empty());

    // all done
    return 0;
}


// end of file
