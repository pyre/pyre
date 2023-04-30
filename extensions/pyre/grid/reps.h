// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_reps_h)
#define pyre_py_grid_reps_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // endow {repT} with the basic methods from {pyre::grid::rep_t} and {pyre::grid::product_t}
    template <class repT>
    void reps(py::class_<repT> &);

} // namespace pyre::py::grid


// get the implementation
#define pyre_py_grid_reps_icc
#include "reps.icc"
#undef pyre_py_grid_reps_icc

#endif

// end of file
