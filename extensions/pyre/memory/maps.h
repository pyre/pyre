// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::memory {
    // class record factories
    template <class cellT>
    void map(py::module &, classname_t, docstring_t);

    template <class cellT>
    void constmap(py::module &, classname_t, docstring_t);

} // namespace pyre::py::memory


// get the inline definitions
#include "maps.icc"


// end of file
