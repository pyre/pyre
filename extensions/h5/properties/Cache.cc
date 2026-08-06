// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the caches a file reaches its data through
void
pyre::h5::py::properties::cache(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<Cache>(
        // in scope
        m,
        // class name
        "Cache",
        // docstring
        "the caches a file reaches its data through");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<int, std::size_t, std::size_t, double>(),
        // the signature
        "metadataElements"_a, "slots"_a, "bytes"_a, "preemption"_a,
        // the docstring
        "describe the caches a file reaches its data through");

    // how many entries the metadata cache holds
    cls.def_readwrite(
        // the name
        "metadataElements",
        // the field
        &Cache::metadataElements,
        // the docstring
        "how many entries the metadata cache holds");

    // the number of slots in the hash table that indexes cached chunks
    cls.def_readwrite(
        // the name
        "slots",
        // the field
        &Cache::slots,
        // the docstring
        "the number of slots in the hash table that indexes cached chunks");

    // how much memory the chunk cache may hold
    cls.def_readwrite(
        // the name
        "bytes",
        // the field
        &Cache::bytes,
        // the docstring
        "how much memory the chunk cache may hold");

    // how strongly to favor evicting a fully used chunk
    cls.def_readwrite(
        // the name
        "preemption",
        // the field
        &Cache::preemption,
        // the docstring
        "how strongly to favor evicting a fully used chunk");

    // all done
    return;
}


// end of file
