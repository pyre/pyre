// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::memory {
    // class record factory
    template <class cellT>
    void heap(py::module &, classname_t, docstring_t);
} // namespace pyre::py::memory


// get the inline definitions
#include "heaps.icc"


// end of file
