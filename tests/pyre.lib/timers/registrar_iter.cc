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


// exercise iterating through the index contents
int main() {
    // make an index
    registrar_t registrar;

    // lookup a name
    registrar.lookup("test.registrar.1");
    // and another one
    registrar.lookup("test.registrar.2");

    // initialize the count
    std::size_t count = 0;
    // go through the contents
    for (auto & [name, movement] : registrar) {
        // verify the timer activation state is as expected
        assert(movement.active() == false);
        // increment the counter
        count++;
    }
    // verify that we went through all the timers
    assert(count == registrar.size());

    // all done
    return 0;
}


// end of file
