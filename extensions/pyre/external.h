// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_py_external_h)
#define pyre_py_external_h


// stl
#include <complex>

// pybind support
#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>


// get the pyre parts
#include <pyre/memory.h>
#include <pyre/timers.h>


// type aliases
namespace pyre::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;

    // memory types
    // complex of float
    using map_c4_t = pyre::memory::map_t<std::complex<float>>;
    using constmap_c4_t = pyre::memory::constmap_t<std::complex<float>>;
    // complex of double
    using map_c8_t = pyre::memory::map_t<std::complex<double>>;
    using constmap_c8_t = pyre::memory::constmap_t<std::complex<double>>;
} // namespace pyre::py


#endif

// end of file
