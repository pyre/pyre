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


// verify that looking up timer names in the index creates the associated shared state
int main() {
    // make a registry
    registrar_t registrar;

    // lookup a couple of names
    registrar.lookup("test.registrar.1");
    registrar.lookup("test.registrar.2");

    // make sure the index contains two names
    assert (registrar.size() == 2);
    // and that our names are the only ones there
    assert (registrar.contains("test.registrar.1"));
    assert (registrar.contains("test.registrar.2"));

    // all done
    return 0;
}


// end of file
