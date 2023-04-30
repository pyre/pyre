// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_cuda_memory_externals_h)
#define pyre_cuda_memory_externals_h


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
}


#endif

// end of file
