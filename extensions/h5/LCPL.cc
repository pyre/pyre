// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// link creation property lists
void
pyre::h5::py::lcpl(py::module & m)
{
    // add bindings for link creation property lists
    auto cls = py::class_<LCPL, PropList>(
        // in scope
        m,
        // class name
        "LCPL",
        // docstring
        "a link creation property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) {
            // easy enough
            return &LCPL::DEFAULT;
        },
        // docstring
        "the default link creation property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a link creation property list");

    // interface
#if H5_VERSION_GE(1, 12, 0)
    // MGA: this is my best guess as to how far this was back-ported
    // set the intermediate group creation strategy
    cls.def(
        // the name
        "getCreateIntermediateGroup",
        // the implementation
        &LCPL::getCreateIntermediateGroup,
        // the docstring
        "get the intermediate group creation strategy");
    // set the intermediate group creation strategy
    cls.def(
        // the name
        "setCreateIntermediateGroup",
        // the implementation
        &LCPL::setCreateIntermediateGroup,
        // the signature
        "create"_a,
        // the docstring
        "set the intermediate group creation strategy");
#endif

    // set the string character encoding
    cls.def(
        // the name
        "getCharEncoding",
        // the implementation
        &LCPL::getCharEncoding,
        // the docstring
        "get the string character encoding");
    // set the string character encoding
    cls.def(
        // the name
        "setCharEncoding",
        // the implementation
        &LCPL::setCharEncoding,
        // the signature
        "encoding"_a,
        // the docstring
        "set the string character encoding");

    // all done
    return;
}


// end of file
