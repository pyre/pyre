// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(h5_py_forward_h)
#define h5_py_forward_h


// the {h5} extension namespace
namespace pyre::h5::py {
    // the module api
    void api(py::module &);

    // wrappers for C++ api
    void dataspace(py::module &);
    void dataset(py::module &);
    void file(py::module &);
    void group(py::module &);

} // namespace pyre::h5::py


// datatypes are in their own namespace
namespace pyre::h5::py::datatypes {
    // datatypes
    void datatypes(py::module &);
} // namespace pyre::h5::py::datatypes


// file access parameter lists are in their own namespace
namespace pyre::h5::py::fapls {
    // fapls
    void fapls(py::module &);
} // namespace pyre::h5::py::fapls

#endif

// end of file
