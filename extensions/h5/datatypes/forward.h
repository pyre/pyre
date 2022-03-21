// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(h5_py_datatypes_forward_h)
#define h5_py_datatypes_forward_h


// the local binders
namespace h5::py::datatypes {
    // the module intializer
    void datatypes(py::module &);

    // datatype classes
    void datatype(py::module &);
    void compound(py::module &);
    void predefined(py::module &);

    // constants
    void native(py::module &);

} // namespace h5::py::datatypes


#endif

// end of file
