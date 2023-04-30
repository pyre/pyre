// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_orders_h)
#define pyre_py_grid_orders_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the order instantiations
    void order2d(py::module &);
    void order3d(py::module &);
    void order4d(py::module &);

    // the interface decorator
    template <class orderT>
    void orderInterface(py::class_<orderT> &);

} // namespace pyre::py::grid


#endif

// end of file
