// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_algebra_h)
#define pyre_py_grid_algebra_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // endow {repT} with an algebra
    template <class repT>
    void algebra(py::class_<repT> &);

} // namespace pyre::py::grid


// get the implementation
#define pyre_py_grid_algebra_icc
#include "algebra.icc"
#undef pyre_py_grid_algebra_icc

#endif

// end of file
