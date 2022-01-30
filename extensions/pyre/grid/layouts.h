// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_py_grid_layouts_h)
#define pyre_py_grid_layouts_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the layout instantiations
    void canonical2d(py::module &);
    void canonical3d(py::module &);
    void canonical4d(py::module &);

    // the interface decorator
    template <class layoutT>
    void layoutInterface(py::class_<layoutT> &);

} // namespace pyre::py::grid


#endif

// end of file
