// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::grid {
    // endow {repT} with the basic methods from {pyre::grid::rep_t} and {pyre::grid::product_t}
    template <class repT>
    void reps(py::class_<repT> &);

} // namespace pyre::py::grid


// get the inline definitions
#include "reps.icc"


// end of file
