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
pyre::h5::py::properties::cacheClass(py::module & m)
{
    // register the class of the record
    py::class_<Cache>(
        // in scope
        m,
        // class name
        "Cache",
        // docstring
        "the caches a file reaches its data through");

    // all done
    return;
}


// the caches a file reaches its data through
void
pyre::h5::py::properties::cache()
{
    // the class, registered by {cacheClass}
    auto cls = py::class_<Cache>(py::type::of<Cache>());

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<int, std::size_t, std::size_t, double>(),
        // the signature
        "metadataElements"_a, "slots"_a, "bytes"_a, "preemption"_a,
        // the docstring
        "describe the caches a file reaches its data through");

    // how many entries the metadata cache holds
    cls.def_property(
        // the name
        "metadataElements",
        // the getter
        pyre::py::getter(cls, &Cache::metadataElements),
        // the setter
        pyre::py::setter(cls, &Cache::metadataElements),
        // the docstring
        "how many entries the metadata cache holds");

    // the number of slots in the hash table that indexes cached chunks
    cls.def_property(
        // the name
        "slots",
        // the getter
        pyre::py::getter(cls, &Cache::slots),
        // the setter
        pyre::py::setter(cls, &Cache::slots),
        // the docstring
        "the number of slots in the hash table that indexes cached chunks");

    // how much memory the chunk cache may hold
    cls.def_property(
        // the name
        "bytes",
        // the getter
        pyre::py::getter(cls, &Cache::bytes),
        // the setter
        pyre::py::setter(cls, &Cache::bytes),
        // the docstring
        "how much memory the chunk cache may hold");

    // how strongly to favor evicting a fully used chunk
    cls.def_property(
        // the name
        "preemption",
        // the getter
        pyre::py::getter(cls, &Cache::preemption),
        // the setter
        pyre::py::setter(cls, &Cache::preemption),
        // the docstring
        "how strongly to favor evicting a fully used chunk");

    // all done
    return;
}


// end of file
