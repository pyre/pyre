// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(h5_py_forward_h)
#define h5_py_forward_h


// the {h5} extension namespace
namespace pyre::h5::py {
    // the module api
    void api(py::module &);

    // wrappers for the C++ HDF5 api
    // support
    void enums(py::module &);
    // property lists
    void pl(py::module &);
    void dapl(py::module &);
    void dcpl(py::module &);
    void dxpl(py::module &);
    void fapl(py::module &);
    void fcpl(py::module &);
    void lapl(py::module &);
    void lcpl(py::module &);
    // datasets
    void dataspace(py::module &);
    void dataset(py::module &);
    // structural
    void group(py::module &);
    void file(py::module &);
} // namespace pyre::h5::py


#endif

// end of file
