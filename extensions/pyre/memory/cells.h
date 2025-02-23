// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"


namespace pyre::py::memory::cells {
    // the pybind11 class record
    template <typename cellT>
    using pycell_t = py::class_<cellT>;

    // the type registrar
    template <class... cellT>
    inline auto expand(py::module &, pyre::typelists::types_t<cellT...> &&) -> void;

    // the cell type record builder
    template <class cellT>
    inline auto cell(py::module & m) -> void;

    // the class docstring
    template <class cellT>
    inline auto docstring() -> string_t;

    // constructors
    template <class cellT>
    inline auto constructors(pycell_t<cellT> &) -> void;

    // accessors
    template <class cellT>
    inline auto accessors(pycell_t<cellT> &) -> void;

} // namespace pyre::py::memory::cells


// implementations
#include "cells.icc"


// end of file
