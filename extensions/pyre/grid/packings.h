// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_packings_h)
#define pyre_py_grid_packings_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the packing instantiations
    void canonical2d(py::module &);
    void canonical3d(py::module &);
    void canonical4d(py::module &);

    // the interface decorator
    template <class packingT>
    void packingInterface(py::class_<packingT> &);

} // namespace pyre::py::grid


#endif

// end of file
