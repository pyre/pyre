// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the standard library
#include <cstdint>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
// the cuda runtime
#include <cuda_runtime.h>
// the cuda libraries
#include <cublas_v2.h>
#include <cusolverDn.h>
#include <curand.h>
// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
// pyre
#include <pyre/journal.h>
#include <pyre/grid.h>
#include <pyre/memory.h>


// type aliases
namespace pyre::cuda::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;
    // strings
    using string_t = std::string;
} // namespace pyre::cuda::py


// end of file
