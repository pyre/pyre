// -*- C++ -*-
// -*- coding: utf-8 -*-
//

// code guard
#if !defined(pyre_cuda_ComputeCapability_h)
#define pyre_cuda_ComputeCapability_h

#include <iostream>
#include <string>

// CUDA device compute capability
//
// ComputeCapability identifies a CUDA device's architecture generation and
// feature compatibility.
struct pyre::cuda::ComputeCapability {
    // Construct a new ComputeCapability object.
    constexpr ComputeCapabiltiy(int major, int minor) noexcept;

    explicit operator std::string() const;

    int major; // Major compute version
    int minor; // Minor compute version
};

// Serialize ComputeCapability object to stream
std::ostream &
pyre::cuda::
operator<<(std::ostream &, pyre::cuda::ComputeCapability);

// Compare two ComputeCapability objects.
constexpr bool
pyre::cuda::
operator==(pyre::cuda::ComputeCapability,
           pyre::cuda::ComputeCapability) noexcept;

// Compare two ComputeCapability objects.
constexpr bool
pyre::cuda::
operator!=(pyre::cuda::ComputeCapability,
           pyre::cuda::ComputeCapability) noexcept;

// Compare two ComputeCapability objects.
constexpr bool
pyre::cuda::
operator<(pyre::cuda::ComputeCapability,
          pyre::cuda::ComputeCapability) noexcept;

// Compare two ComputeCapability objects.
constexpr bool
pyre::cuda::
operator>(pyre::cuda::ComputeCapability,
          pyre::cuda::ComputeCapability) noexcept;

// Compare two ComputeCapability objects.
constexpr bool
pyre::cuda::
operator<=(pyre::cuda::ComputeCapability,
           pyre::cuda::ComputeCapability) noexcept;

// Compare two ComputeCapability objects.
constexpr bool
pyre::cuda::
operator>=(pyre::cuda::ComputeCapability,
           pyre::cuda::ComputeCapability) noexcept;

#endif

// end of file
