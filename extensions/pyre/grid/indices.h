// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_grid_indices_h)
#define pyre_py_grid_indices_h


// the {pyre} extension namespace
namespace pyre::py::grid {
    // the index instantiations
    void index2d(py::module &);
    void index3d(py::module &);
    void index4d(py::module &);

    // the interface decorator
    template <class indexT>
    void indexInterface(py::class_<indexT> &);

} // namespace pyre::py::grid


#endif

// end of file
