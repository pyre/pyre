// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// external dependencies
#include "../external.h"
// namespace setup
#include "../forward.h"


// build the submodule
void
pyre::py::timers(py::module & m)
{
    auto timers = m.def_submodule(
        // the name
        "timers",
        // its docstring
        "support for timers");

    // get the timer bindings
    pyre::py::wall_timers(timers);
    pyre::py::process_timers(timers);
}


// end of file
