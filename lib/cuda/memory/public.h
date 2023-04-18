// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_cuda_memory_public_h)
#define pyre_cuda_memory_public_h


// external packages
#include "externals.h"
// get the forward declarations
#include "forward.h"

// published type aliases; this is the file you are looking for...
#include "api.h"

// implementation
// managed memory
#include "Managed.h"

// pinned memory
#include "HostPinned.h"

// mapped memory
#include "HostMapped.h"

// benchmark kernel
#include "benchmark_kernel.h"

#endif

// end of file
