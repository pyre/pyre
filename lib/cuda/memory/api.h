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

    // export host pinned memory blocks
    // read/write access
    template <typename T>
    using host_pinned_t = HostPinned<T, false>;

    // read-only access
    template <typename T>
    using consthost_pinned_t = HostPinned<T, true>;

    // export device pinned memory blocks
    // read/write access
    template <typename T>
    using device_pinned_t = DevicePinned<T, false>;

    // read-only access
    template <typename T>
    using constdevice_pinned_t = DevicePinned<T, true>;

    // export host mapped memory blocks
    // read/write access
    template <typename T>
    using host_mapped_t = HostMapped<T, false>;

    // read-only access
    template <typename T>
    using consthost_mapped_t = HostMapped<T, true>;

    // export device mapped memory blocks
    // read/write access
    template <typename T>
    using device_mapped_t = DeviceMapped<T, false>;

    // read-only access
    template <typename T>
    using constdevice_mapped_t = DeviceMapped<T, true>;
} // namespace pyre::cuda::memory


#endif

// end of file
