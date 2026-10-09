// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// get the journal
#include <pyre/journal.h>

// pybind support
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
// pyre is built against pybind11 3.0 or later
static_assert(PYBIND11_VERSION_MAJOR >= 3, "pyre requires pybind11 3.0 or later");

// make certain STL containers opaque
PYBIND11_MAKE_OPAQUE(pyre::journal::page_t);
PYBIND11_MAKE_OPAQUE(pyre::journal::notes_t);


// type aliases
namespace pyre::journal::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;
} // namespace pyre::journal::py


// end of file
