// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include <bit>
#include <string>

// the format codes describe cells to the python buffer protocol, so this layer depends on
// pybind11 by construction; it is the python-support tier of the library, never included by
// the pure c++ surface
#include <pybind11/pybind11.h>
#include <pybind11/complex.h>

// the cell types being described
#include <pyre/memory.h>


// type aliases
namespace pyre::py {
    // import {pybind11}
    namespace py = pybind11;
    // strings
    using string_t = std::string;
} // namespace pyre::py


// end of file
