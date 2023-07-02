// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// dataset memory transfer property lists
void
pyre::h5::py::dxpl(py::module & m)
{
    // add bindings for hdf5 dataset memory transfer property lists
    auto cls = py::class_<DXPL, PropList>(
        // in scope
        m,
        // class name
        "DXPL",
        // docstring
        "a dataset memory transfer property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) {
            // easy enough
            return &DXPL::DEFAULT;
        },
        // docstring
        "the default dataset memory transfer property list");

    // constructors
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a dataset memory transfer property list");

    cls.def(
        // the implementation
        py::init<const char *>(),
        // the signature
        "expression"_a,
        // the docstring
        "build a dataset memory transfer property list");

    // all done
    return;
}


// end of file
