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
pyre::h5::py::properties::pageBufferClass(py::module & m)
{
    // register the class of the record
    py::class_<PageBuffer>(
        // in scope
        m,
        // class name
        "PageBuffer",
        // docstring
        "the buffer a paged file gathers its pages in");

    // all done
    return;
}


// the buffer a paged file gathers its pages in
void
pyre::h5::py::properties::pageBuffer()
{
    // the class, registered by {pageBufferClass}
    auto cls = py::class_<PageBuffer>(py::type::of<PageBuffer>());

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<std::size_t, unsigned int, unsigned int>(),
        // the signature
        "bytes"_a, "metadata"_a, "raw"_a,
        // the docstring
        "describe the buffer a paged file gathers its pages in");

    // how much memory the buffer may hold
    cls.def_property(
        // the name
        "bytes",
        // the getter
        pyre::py::getter(cls, &PageBuffer::bytes),
        // the setter
        pyre::py::setter(cls, &PageBuffer::bytes),
        // the docstring
        "how much memory the buffer may hold");

    // the smallest share reserved for metadata pages
    cls.def_property(
        // the name
        "metadata",
        // the getter
        pyre::py::getter(cls, &PageBuffer::metadata),
        // the setter
        pyre::py::setter(cls, &PageBuffer::metadata),
        // the docstring
        "the smallest share reserved for metadata pages");

    // the smallest share reserved for raw data pages
    cls.def_property(
        // the name
        "raw",
        // the getter
        pyre::py::getter(cls, &PageBuffer::raw),
        // the setter
        pyre::py::setter(cls, &PageBuffer::raw),
        // the docstring
        "the smallest share reserved for raw data pages");

    // all done
    return;
}


// end of file
