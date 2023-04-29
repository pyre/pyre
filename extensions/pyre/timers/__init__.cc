// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// package declarations
#include "__init__.h"

// build the submodule
void
pyre::py::timers::__init__(py::module & m)
{
    // create a submodule
    auto timers = m.def_submodule(
        // the name
        "timers",
        // its docstring
        "support for timers");

    // install the timer bindings
    wall_timers(timers);
    process_timers(timers);
}


// end of file
