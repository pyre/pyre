// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// STL
#include <string>
#include <vector>
// support
#include <pyre/journal.h>
// the library we wrap
#include <gsl/gsl_errno.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


// type aliases
namespace gsl::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals, so that argument names can be spelled "name"_a
    using namespace py::literals;

    // for decorating pybind11 classes
    // class names
    using classname_t = const char *;
    // docstrings
    using docstring_t = const char *;
} // namespace gsl::py


// end of file
