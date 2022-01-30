// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_py_grid_forward_h)
#define pyre_py_grid_forward_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the initializer
    void grid(py::module &);

    // indices
    void indices(py::module &);
    // shapes
    void shapes(py::module &);

} // namespace pyre::py::grid


#endif

// end of file
