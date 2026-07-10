// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// STL
#include <cstdint>
#include <optional>
#include <string>
#include <utility>
#include <vector>
// support
#include <pyre/journal.h>
#include <pyre/postgres.h>
// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


// type aliases
namespace pyre::postgres::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals, so that argument names can be spelled "name"_a
    using namespace py::literals;

    // for decorating pybind11 classes
    // class names
    using classname_t = const char *;
    // docstrings
    using docstring_t = const char *;

    // the entities of {pyre::postgres} are all visible here without qualification, since this
    // namespace is nested inside theirs
} // namespace pyre::postgres::py


// end of file
