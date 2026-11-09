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
pyre::h5::py::properties::laplClass(py::module & m)
{
    // register the class of link access property lists
    py::class_<LAPL, PropList>(
        // in scope
        m,
        // class name
        "lapl",
        // docstring
        "a link access property list");

    // all done
    return;
}


// link access property lists
void
pyre::h5::py::properties::lapl()
{
    // the class, registered by {laplClass}
    auto cls = py::class_<LAPL, PropList>(py::type::of<LAPL>());

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const LAPL & {
            // easy enough
            return LAPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default link access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a link access property list");

    // interface
    // the number of allowed link traversals
    cls.def_property(
        // the name
        "traversalLimit",
        // the getter
        py::overload_cast<>(py::overload_cast<>(&LAPL::traversalLimit, py::const_), py::const_),
        // the setter
        pyre::py::setter(cls, py::overload_cast<std::size_t>(&LAPL::traversalLimit)),
        // the docstring
        "how many links i will follow before declaring a cycle");

    // the prefix prepended to external link filenames
    cls.def_property(
        // the name
        "externalPrefix",
        // the getter
        py::overload_cast<>(&LAPL::externalPrefix, py::const_),
        // the setter
        pyre::py::setter(cls, py::overload_cast<const string_t &>(&LAPL::externalPrefix)),
        // the docstring
        "the prefix prepended to the filename an external link names");

    // all done
    return;
}


// end of file
