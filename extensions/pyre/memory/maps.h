// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// external
#include "external.h"


// the {pyre} extension namespace
namespace pyre::py::memory::maps {
    // the pybind11 class record
    template <typename mapT>
    using pymap_t = pymem_t<mapT>;

    // the type registrar
    template <class... mapT>
    inline auto expand(py::module &, pyre::typelists::types_t<mapT...> &&) -> void;

    // the map record builder
    template <class mapT>
    inline auto map(py::module &) -> void;

    // the class docstring
    template <class mapT>
    inline auto docstring() -> string_t;

    // constructors
    template <class mapT>
    inline auto constructors(pymap_t<mapT> &) -> void;

} // namespace pyre::py::memory::maps


// implementations
#include "maps.icc"


// end of file
