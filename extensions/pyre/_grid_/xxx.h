// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// package declarations
#include "__init__.h"


// the multidimensional index expansions
namespace pyre::py::_grid_::xxx {
    // the pybind11 class record
    template <typename xxxT>
    using pyindex_t = py::class_<xxxT>;

    // the type registrar
    template <class... xxxT>
    inline auto expand(py::module, pyre::typelists::types_t<xxxT...> &&) -> void;

    // the index record builder

    // the class docstring

    // constructors

} // namespace pyre::py::_grid_::xxx


// implementations
#include "xxx.icc"


// end of file
