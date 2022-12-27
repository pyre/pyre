// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_forward_h)
#define pyre_py_grid_forward_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the initializer
    void grid(py::module &);

    // indices
    void indices(py::module &);
    // orders
    void orders(py::module &);
    // shapes
    void shapes(py::module &);
    // packings
    void packings(py::module &);
    // grids
    void grids(py::module &);
} // namespace pyre::py::grid


#endif

// end of file
