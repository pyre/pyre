// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// external
#include "external.h"


// the {pyre} extension namespace
namespace pyre::py::memory::heaps {
    // the pybind11 class record
    template <typename heapT>
    using pyheap_t = pymem_t<heapT>;

    // the type registrar
    template <class... heapT>
    inline auto expand(py::module &, pyre::typelists::types_t<heapT...> &&) -> void;

    // the heap record builder
    template <class heapT>
    inline auto heap(py::module &) -> void;

    // the class docstring
    template <class heapT>
    inline auto docstring() -> string_t;

    // constructors
    template <class heapT>
    inline auto constructors(pyheap_t<heapT> &) -> void;
} // namespace pyre::py::memory::heaps


// implementations
#include "heaps.icc"


// end of file
