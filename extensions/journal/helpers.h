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

    // the setters of the properties of the class bound by {cls}, with their parameter named
    // {value}; the journal sits below libpyre, so it keeps its own copy of these helpers
    // made from a method
    template <class classT, class returnT, class ownerT, class argT, bool except>
    inline auto setter(const classT & cls, returnT (ownerT::*method)(argT) noexcept(except))
        -> py::cpp_function;
    // made from a callable that takes an instance of the class bound by {cls} and the new value
    template <class classT, class callableT>
    inline auto setter(const classT & cls, callableT callable) -> py::cpp_function;
} // namespace pyre::journal::py


// get the inline definitions
#include "helpers.icc"


// end of file
