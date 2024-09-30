// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


// code guard
#if !defined(h5_py_data_h)
#define h5_py_data_h

// this decorator captures part of the H5::Object interface
// it is necessary because H5::Object is abstract and cannot be bound

// extend the pyre::h5::py namespace
namespace pyre::h5::py {
    // decorator that adds data accessors to the attributes of an h5 object
    template <class objectT>
    void data(py::class_<objectT> &);

} // namespace pyre::h5::py

// get the implementation
#define h5_py_data_icc
#include "data.icc"
#undef h5_py_data_icc


#endif

// end of file
