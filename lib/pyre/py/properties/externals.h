// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the accessors are pybind11 functions, so this layer depends on pybind11 by construction; it is
// the python-support tier of the library, never included by the pure c++ surface
#include <type_traits>
#include <pybind11/pybind11.h>


// type aliases
namespace pyre::py {
    // import {pybind11}
    namespace py = pybind11;
} // namespace pyre::py


// end of file
