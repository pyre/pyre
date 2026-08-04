// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// link creation property lists
void
pyre::h5::py::properties::lcpl(py::module & m)
{
    // add bindings for link creation property lists
    auto cls = py::class_<LCPL, STRCPL>(
        // in scope
        m,
        // class name
        "lcpl",
        // docstring
        "a link creation property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const LCPL & {
            // easy enough
            return LCPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default link creation property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a link creation property list");

    // interface
    // whether missing intermediate groups are created on demand
    cls.def_property(
        // the name
        "createIntermediateGroup",
        // the getter
        &LCPL::createIntermediateGroup,
        // the setter
        &LCPL::setCreateIntermediateGroup,
        // the docstring
        "whether the groups along a path i am given are created when they are missing");

    // all done
    return;
}


// end of file
