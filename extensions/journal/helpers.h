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
} // namespace pyre::journal::py


// get the inline definitions
#include "helpers.icc"


// end of file
