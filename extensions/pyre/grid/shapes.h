// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_shapes_h)
#define pyre_py_grid_shapes_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the shape instantiations
    void shape2d(py::module &);
    void shape3d(py::module &);
    void shape4d(py::module &);

    // the interface decorator
    template <class shapeT>
    void shapeInterface(py::class_<shapeT> &);

} // namespace pyre::py::grid


#endif

// end of file
