// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// the {pyre} extension namespace
namespace pyre::py::grid {
    // endow {repT} with an algebra
    template <class repT>
    void algebra(py::class_<repT> &);

} // namespace pyre::py::grid


// get the implementation
#include "algebra.icc"


// end of file
