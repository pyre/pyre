// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include <cstddef>
#include <functional>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
// the type-erased closures lift cells into python and describe blocks to the buffer
// protocol, so this layer depends on pybind11 by construction; it is the python-support
// tier of the library, never included by the pure c++ surface
#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>
// the grid vocabulary and the storage strategies the erased classes travel over
#include <pyre/grid.h>
#include <pyre/memory.h>
// the buffer protocol description of a cell type
#include <pyre/py/memory/format.h>


// type aliases
namespace pyre::py {
    // import {pybind11}
    namespace py = pybind11;
    // strings
    using string_t = std::string;
} // namespace pyre::py


// end of file
