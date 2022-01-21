// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the module entry point
PYBIND11_MODULE(pyre, m)
{
    // the docstring
    m.doc() = "the pyre extension module";

    // register the module api
    pyre::py::api(m);

    // get the timer bindings
    pyre::py::timers(m);
}


// end of file
