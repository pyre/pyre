// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// STL
#include <cstdint>
#include <complex>
#include <string>
// support
#include <pyre/journal.h>
// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>


// type aliases
namespace pyre::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;

    // basic types
    using size_t = std::size_t;
    using string_t = std::string;

    // for decorating pybind11 classes
    // class names
    using classname_t = const char *;
    // docstrings
    using docstring_t = const char *;

    // wrapper to install a {std::shared_ptr} as the custom holder for the bindings
    template <class clsT>
    using shared_holder_t = py::class_<clsT, std::shared_ptr<clsT>>;

} // namespace pyre::py


// end of file
