// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_cuda_memory_api_h)
#define pyre_cuda_memory_api_h


// user facing types
namespace pyre::cuda::memory {
    // export managed memory blocks
    // read/write access
    template <typename T>
    using managed_t = Managed<T, false>;

    // read-only access
    template <typename T>
    using constmanaged_t = Managed<T, true>;

    // export pinned memory blocks
    // read/write access
    template <typename T>
    using pinned_t = Pinned<T, false>;

    // read-only access
    template <typename T>
    using constpinned_t = Pinned<T, true>;

    // export mapped memory blocks
    // read/write access
    template <typename T>
    using mapped_t = Mapped<T, false>;

    // read-only access
    template <typename T>
    using constmapped_t = Mapped<T, true>;
} // namespace pyre::cuda::memory


#endif

// end of file
