// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the buffer a paged file gathers its pages in
void
pyre::h5::py::properties::pageBuffer(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<PageBuffer>(
        // in scope
        m,
        // class name
        "PageBuffer",
        // docstring
        "the buffer a paged file gathers its pages in");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<std::size_t, unsigned int, unsigned int>(),
        // the signature
        "bytes"_a, "metadata"_a, "raw"_a,
        // the docstring
        "describe the buffer a paged file gathers its pages in");

    // how much memory the buffer may hold
    cls.def_readwrite(
        // the name
        "bytes",
        // the field
        &PageBuffer::bytes,
        // the docstring
        "how much memory the buffer may hold");

    // the smallest share reserved for metadata pages
    cls.def_readwrite(
        // the name
        "metadata",
        // the field
        &PageBuffer::metadata,
        // the docstring
        "the smallest share reserved for metadata pages");

    // the smallest share reserved for raw data pages
    cls.def_readwrite(
        // the name
        "raw",
        // the field
        &PageBuffer::raw,
        // the docstring
        "the smallest share reserved for raw data pages");

    // all done
    return;
}


// end of file
