// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// register the class, so that every signature can name it
void
pyre::h5::py::properties::lcplClass(py::module & m)
{
    // register the class of link creation property lists
    py::class_<LCPL, STRCPL>(
        // in scope
        m,
        // class name
        "lcpl",
        // docstring
        "a link creation property list");

    // all done
    return;
}


// link creation property lists
void
pyre::h5::py::properties::lcpl()
{
    // the class, registered by {lcplClass}
    auto cls = py::class_<LCPL, STRCPL>(py::type::of<LCPL>());

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
        "intermediateGroupCreation",
        // the getter
        py::overload_cast<>(&LCPL::intermediateGroupCreation, py::const_),
        // the setter
        pyre::py::setter(cls, py::overload_cast<bool>(&LCPL::intermediateGroupCreation)),
        // the docstring
        "whether the groups along a path i am given are created when they are missing");

    // all done
    return;
}


// end of file
