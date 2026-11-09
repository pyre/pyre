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
pyre::h5::py::properties::strcplClass(py::module & m)
{
    // register the class of the properties shared by everything that lays down a name; there is
    // no constructor, since these settings are always part of a concrete list
    py::class_<STRCPL, PropList>(
        // in scope
        m,
        // class name
        "strcpl",
        // docstring
        "the properties shared by everything that lays down a name");

    // all done
    return;
}


// string creation property lists
void
pyre::h5::py::properties::strcpl()
{
    // the class, registered by {strcplClass}
    auto cls = py::class_<STRCPL, PropList>(py::type::of<STRCPL>());

    // interface
    // the character set the names are recorded in
    cls.def_property(
        // the name
        "charEncoding",
        // the getter
        py::overload_cast<>(&STRCPL::charEncoding, py::const_),
        // the setter
        py::overload_cast<H5T_cset_t>(&STRCPL::charEncoding),
        // the docstring
        "the character set the names i create are recorded in");

    // all done
    return;
}


// end of file
