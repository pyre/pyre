// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


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

    // grid
    pyre::py::grid::grid(m);
    // memory
    pyre::py::memory::memory(m);
    // timers
    pyre::py::timers::timers(m);
    // viz
    pyre::py::viz::viz(m);
}


// end of file
