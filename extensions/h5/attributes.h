// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


// code guard
#if !defined(h5_py_attributes_h)
#define h5_py_attributes_h

// this decorator captures part of the H5::Object interface
// it is necessary because H5::Object is abstract and cannot be bound

// extend the pyre::h5::py namespace
namespace pyre::h5::py {
    // decorator that adds access to the attributes of an h5 object
    template <class objectT>
    void attributes(py::class_<objectT> &);

} // namespace pyre::h5::py

// get the implementation
#define h5_py_attributes_icc
#include "attributes.icc"
#undef h5_py_attributes_icc


#endif

// end of file
