// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// what a group expects to hold, so its object header is sized for it
void
pyre::h5::py::properties::linkEstimate(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<LinkEstimate>(
        // in scope
        m,
        // class name
        "LinkEstimate",
        // docstring
        "what a group expects to hold, so its object header is sized for it");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<unsigned int, unsigned int>(),
        // the signature
        "links"_a, "nameLength"_a,
        // the docstring
        "describe what a group expects to hold, so its object header is sized for it");

    // how many members the group expects
    cls.def_readwrite(
        // the name
        "links",
        // the field
        &LinkEstimate::links,
        // the docstring
        "how many members the group expects");

    // how long their names run, on average
    cls.def_readwrite(
        // the name
        "nameLength",
        // the field
        &LinkEstimate::nameLength,
        // the docstring
        "how long their names run, on average");

    // all done
    return;
}


// end of file
