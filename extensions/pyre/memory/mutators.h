// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"
// local declarations
#include "__init__.h"


// decorator that adds the write access common to all writable storage strategies
namespace pyre::py::memory {
    // write access
    template <class memT>
    auto mutators(pymem_t<memT> &) -> void;
} // namespace pyre::py::memory


// implementations
#include "mutators.icc"


// end of file
