// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#if !defined(pyre_cuda_memory_forward_h)
#define pyre_cuda_memory_forward_h


// set up the namespace
namespace pyre::cuda::memory {
    // managed memory block on the device with universal access
    template <typename T, bool isConst>
    class Managed;
}; // namespace pyre::cuda::memory


#endif

// end of file
