// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"


// decorator that adds properties common to all storage strategies
namespace pyre::py::memory {
    template <class T>
    auto properties(pymem_t<T> &) -> void;
}


// implementations
#include "properties.icc"


// end of file
