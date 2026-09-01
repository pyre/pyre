// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// one chunk of a chunked dataset, as it exists in the file
void
pyre::h5::py::chunk(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<Chunk>(
        // in scope
        m,
        // class name
        "Chunk",
        // docstring
        "one chunk of a chunked dataset, as it exists in the file");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<index_t, unsigned int, haddr_t, hsize_t>(),
        // the signature
        "origin"_a, "filterMask"_a, "address"_a, "bytes"_a,
        // the docstring
        "describe a chunk that exists in the file");

    // where my first cell sits in the dataset's index space
    cls.def_readwrite(
        // the name
        "origin",
        // the field
        &Chunk::origin,
        // the docstring
        "where my first cell sits in the dataset's index space");

    // which stages of the filter pipeline were skipped when i was written
    cls.def_readwrite(
        // the name
        "filterMask",
        // the field
        &Chunk::filterMask,
        // the docstring
        "which stages of the filter pipeline were skipped when i was written");

    // where i live in the file
    cls.def_readwrite(
        // the name
        "address",
        // the field
        &Chunk::address,
        // the docstring
        "where i live in the file");

    // how much room i take up there, after the pipeline had its way with me
    cls.def_readwrite(
        // the name
        "bytes",
        // the field
        &Chunk::bytes,
        // the docstring
        "my size on disk, after the filter pipeline had its way with me");

    // all done
    return;
}


// end of file
