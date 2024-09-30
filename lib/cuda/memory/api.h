// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#if !defined(pyre_cuda_memory_api_h)
#define pyre_cuda_memory_api_h


// user facing types
namespace pyre::cuda::memory {
    // managed memory
    // read/write
    template <typename T>
    using managed_t = Managed<T, false>;
    // read-only
    template <typename T>
    using constmanaged_t = Managed<T, true>;

    // pinned memory
    // read/write
    template <typename T>
    using pinned_t = Pinned<T, false>;
    // read-only
    template <typename T>
    using constpinned_t = Pinned<T, true>;

    // mapped memory
    // read/write
    template <typename T>
    using mapped_t = Mapped<T, false>;
    // read-only
    template <typename T>
    using constmapped_t = Mapped<T, true>;
} // namespace pyre::cuda::memory


#endif

// end of file
