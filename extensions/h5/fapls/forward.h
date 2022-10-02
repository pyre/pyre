// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(h5_py_fapls_forward_h)
#define h5_py_fapls_forward_h


// the local binders
namespace pyre::h5::py::fapls {
    // the module initializer
    void fapls(py::module &);

    // fapl classes
    void ros3(py::module &);
} // namespace pyre::h5::py::fapls


#endif

// end of file
