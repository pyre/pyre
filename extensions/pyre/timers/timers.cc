// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// build the submodule
void
pyre::py::timers::timers(py::module & m)
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
