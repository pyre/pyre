// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// string creation property lists
void
pyre::h5::py::properties::strcpl(py::module & m)
{
    // add bindings for the properties shared by everything that lays down a name; there is
    // no constructor, since these settings are always part of a concrete list
    auto cls = py::class_<STRCPL, PropList>(
        // in scope
        m,
        // class name
        "strcpl",
        // docstring
        "the properties shared by everything that lays down a name");

    // interface
    // the character set the names are recorded in
    cls.def_property(
        // the name
        "charEncoding",
        // the getter
        &STRCPL::charEncoding,
        // the setter
        &STRCPL::setCharEncoding,
        // the docstring
        "the character set the names i create are recorded in");

    // all done
    return;
}


// end of file
