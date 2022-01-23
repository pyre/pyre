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
    // STL
    // class names
    using classname_t = const char *;
    // docstrings
    using docstring_t = const char *;
} // namespace pyre::py::memory


#endif

// end of file
