// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::memory {
    // bindings for buffers on the heap
    void heaps(py::module &);
    // bindings for file backed storage
    void maps(py::module &);
    // bindings for borrowed memory
    void views(py::module &);
} // namespace pyre::py::memory


// end of file
