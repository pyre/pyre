// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"
// local declarations
#include "__init__.h"


// decorator that adds interface common to all storage strategies
namespace pyre::py::memory {
    // read-only interface
    template <class T>
    auto accessors(pymem_t<T> &) -> void;
} // namespace pyre::py::memory


// implementations
#include "accessors.icc"


// end of file
