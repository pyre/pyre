// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"


namespace pyre::py::memory::cells {
    // the pybind11 class record
    template <typename cellT>
    using pycell_t = py::class_<cellT, pyre::memory::cell_t<void, true>>;

    // the type registrar
    template <class... cellT>
    inline auto expand(py::module &, pyre::typelists::types_t<cellT...> &&) -> void;

    // the cell type record builder
    template <class cellT>
    inline auto cell(py::module & m) -> void;

    // the native order alias registrar
    template <class... T>
    inline auto aliases(py::module &, pyre::typelists::types_t<T...> &&) -> void;
    // the native order alias builder
    template <class T>
    inline auto alias(py::module & m) -> void;

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
