// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(h5_py_forward_h)
#define h5_py_forward_h


// the {h5} extension namespace
namespace h5::py {
    // the module api
    void api(py::module &);

    // datasets
    void dataset(py::module &);
    // files
    void file(py::module &);

} // namespace h5::py


// datatypes are in their own naespace
namespace h5::py::datatypes {
    // datatypes
    void datatypes(py::module &);
} // namespace h5::py::datatypes


#endif

// end of file
