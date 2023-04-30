// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"

// modules
#include "__init__.h"
// subpackages
#include "memory/__init__.h"
#include "grid/__init__.h"
#include "timers/__init__.h"
#include "viz/__init__.h"

// the module entry point
PYBIND11_MODULE(pyre, m)
{
    // the docstring
    m.doc() = "the pyre extension module";

    // register the module api
    pyre::py::api(m);

    // memory
    pyre::py::memory::__init__(m);
    // grid
    pyre::py::grid::__init__(m);
    // timers
    pyre::py::timers::__init__(m);
    // viz
    pyre::py::viz::__init__(m);
}


// end of file
