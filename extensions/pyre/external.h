// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_py_external_h)
#define pyre_py_external_h


// pybind support
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include <pybind11/stl_bind.h>


// get the pyre parts
#include <pyre/timers.h>


// type aliases
namespace pyre::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;
} // namespace pyre::py


#endif

// end of file
