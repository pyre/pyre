// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// where the objects in a file start
void
pyre::h5::py::properties::alignment(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<Alignment>(
        // in scope
        m,
        // class name
        "Alignment",
        // docstring
        "where the objects in a file start");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<hsize_t, hsize_t>(),
        // the signature
        "threshold"_a, "boundary"_a,
        // the docstring
        "describe where the objects in a file start");

    // the size an object must reach before it is placed deliberately
    cls.def_readwrite(
        // the name
        "threshold",
        // the field
        &Alignment::threshold,
        // the docstring
        "the size an object must reach before it is placed deliberately");

    // the multiple such an object starts on
    cls.def_readwrite(
        // the name
        "boundary",
        // the field
        &Alignment::boundary,
        // the docstring
        "the multiple such an object starts on");

    // all done
    return;
}


// end of file
