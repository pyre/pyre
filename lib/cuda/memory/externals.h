// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// cuda
#include <cuda_runtime.h>

// support
#include <pyre/memory.h>
#include <pyre/journal.h>


// aliases that define implementation choices
namespace pyre::memory {
    // sizes of things
    using size_t = std::size_t;
    // distances
    using ptrdiff_t = std::ptrdiff_t;
} // namespace pyre::memory


// end of file
