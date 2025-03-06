// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// external
#include "external.h"


// the {pyre} extension namespace
namespace pyre::py::memory::buffers {
    // the pybind11 class record
    template <typename bufferT>
    using pybuffer_t = shared_holder_t<bufferT>;

    // the type registrar
    template <class... bufferT>
    inline auto expand(py::module &, pyre::typelists::types_t<bufferT...> &&) -> void;

    // the buffer record builder
    template <class bufferT>
    inline auto buffer(py::module &) -> void;

    // the class docstring
    template <class bufferT>
    inline auto docstring() -> string_t;
} // namespace pyre::py::memory::buffers


// implementations
#include "buffers.icc"


// end of file
