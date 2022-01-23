// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_py_memory_external_h)
#define pyre_py_memory_external_h


// get the common ones
#include "../external.h"
// STL
#include <complex>
// pybind support
#include <pybind11/complex.h>
// get the pyre parts
#include <pyre/memory.h>


// type aliases
namespace pyre::py::memory {
    // memory types
    // complex of float
    using map_c4_t = pyre::memory::map_t<std::complex<float>>;
    using constmap_c4_t = pyre::memory::constmap_t<std::complex<float>>;
    // complex of double
    using map_c8_t = pyre::memory::map_t<std::complex<double>>;
    using constmap_c8_t = pyre::memory::constmap_t<std::complex<double>>;
} // namespace pyre::py::memory


#endif

// end of file
