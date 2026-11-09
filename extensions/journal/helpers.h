// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// utilities
namespace pyre::journal::py {
    // build a locator that points to the nearest caller from python
    inline auto locator() -> locator_t;

    // build the python counterpart of the journal exception {error}, an instance of the
    // exception class {type} from {journal.exceptions}
    template <class errorT>
    inline auto complaint(const char * type, const errorT & error) -> py::object;

    // the setter of a property of the class bound by {cls}, with its parameter named {value};
    // the journal sits below libpyre, so it keeps its own copy of this helper
    template <class classT, class methodT>
    inline auto setter(const classT & cls, methodT method) -> py::cpp_function;
} // namespace pyre::journal::py


// get the inline definitions
#include "helpers.icc"


// end of file
