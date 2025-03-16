// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// package declarations
#include "__init__.h"


// the multidimensional index expansions
namespace pyre::py::_grid_::indices {
    // the pybind11 class record
    template <typename indexT>
    using pyindex_t = py::class_<indexT>;

    // the type registrar
    template <class... indexT>
    inline auto expand(py::module &, pyre::typelists::types_t<indexT...> &&) -> void;

    // the index record builder
    template <class indexT>
    inline auto index(py::module &) -> void;

    // the class docstring
    template <class indexT>
    inline auto docstring() -> string_t;

} // namespace pyre::py::_grid_::indices


// implementations
#include "indices.icc"


// end of file
