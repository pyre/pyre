// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(h5_py_datatypes_forward_h)
#define h5_py_datatypes_forward_h


// the local binders
namespace pyre::h5::py::datatypes {
    // the module initializer
    void datatypes(py::module &);

    // datatype classes
    void datatype(py::module &);
    void compound(py::module &);
    void predefined(py::module &);

    // constants
    void native(py::module &);

} // namespace pyre::h5::py::datatypes


#endif

// end of file
