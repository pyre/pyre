// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// get the journal
#include <pyre/journal.h>

// pybind support
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

// make certain STL containers opaque
PYBIND11_MAKE_OPAQUE(pyre::journal::page_t);
PYBIND11_MAKE_OPAQUE(pyre::journal::notes_t);


// type aliases
namespace pyre::journal::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;
}


// end of file
