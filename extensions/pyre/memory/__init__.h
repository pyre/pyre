// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"


// the {memory} subpackage
namespace pyre::py::memory {
    // the package initializer
    auto __init__(py::module &) -> void;
} // namespace pyre::py::memory


// cells
namespace pyre::py::memory::cells {
    // the module initializer
    auto __init__(py::module &) -> void;
} // namespace pyre::py::memory::cells

// bindings for buffers
namespace pyre::py::memory::buffers {
    auto __init__(py::module &) -> void;
}

// bindings for buffers on the heap
namespace pyre::py::memory::heaps {
    auto __init__(py::module &) -> void;
}

// bindings for file backed storage
namespace pyre::py::memory::maps {
    auto __init__(py::module &) -> void;
}

// bindings for borrowed memory
namespace pyre::py::memory::views {
    auto __init__(py::module &) -> void;
} // namespace pyre::py::memory::views


// type aliases
namespace pyre::py::memory {
    template <typename T>
    using pymem_t = py::class_<T, typename T::super_type, std::shared_ptr<T>>;
}


// end of file
