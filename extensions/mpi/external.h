// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// STL
#include <cstddef>
#include <cstdint>
#include <optional>
#include <string>
#include <utility>
#include <vector>
// support
#include <pyre/journal.h>
#include <pyre/mpi.h>
// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


// type aliases
namespace pyre::mpi::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals, so that argument names can be spelled "name"_a
    using namespace py::literals;

    // for decorating pybind11 classes
    // class names
    using classname_t = const char *;
    // docstrings
    using docstring_t = const char *;

    // the entities of {pyre::mpi} are all visible here without qualification, since this
    // namespace is nested inside theirs; the only thing worth naming is the integral type we
    // reduce python's whole numbers as. it must be one of the fixed width types, because those
    // are the only ones {pyre::mpi::datatype} knows: spelling it {long long} would compile here
    // and fail on LP64, where {int64_t} is {long} and the two are distinct types
    using integer_t = std::int64_t;
    // and the type we reduce python's real numbers as
    using real_t = double;
} // namespace pyre::mpi::py


// end of file
