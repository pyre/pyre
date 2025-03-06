// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// external
#include "external.h"


// the {pyre} extension namespace
namespace pyre::py::memory::views {
    // the pybind11 class record
    template <typename viewT>
    using pyview_t = pymem_t<viewT>;

    // the type registrar
    template <class... viewT>
    inline auto expand(py::module &, pyre::typelists::types_t<viewT...> &&) -> void;

    // the view record builder
    template <class viewT>
    inline auto view(py::module &) -> void;

    // the class docstring
    template <class viewT>
    inline auto docstring() -> string_t;

    // constructors
    template <class viewT>
    inline auto constructors(pyview_t<viewT> &) -> void;

} // namespace pyre::py::memory::views


// implementations
#include "views.icc"


// end of file
