// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// link access property lists
void
pyre::h5::py::lapl(py::module & m)
{
    // add bindings for link access property lists
    auto cls = py::class_<LAPL, PropList>(
        // in scope
        m,
        // class name
        "LAPL",
        // docstring
        "a link access property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) {
            // easy enough
            return &LAPL::DEFAULT;
        },
        // docstring
        "the default link access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a link access property list");

    // interface
    // set the number of allowed link traversals
    cls.def(
        // the name
        "getNumLinks",
        // the implementation
        &LAPL::getNumLinks,
        // the docstring
        "get the number of allowed link traversals");
    // set the number of allowed link traversals
    cls.def(
        // the name
        "setNumLinks",
        // the implementation
        &LAPL::setNumLinks,
        // the signature
        "links"_a,
        // the docstring
        "set the number of allowed link traversals");

    // all done
    return;
}


// end of file
