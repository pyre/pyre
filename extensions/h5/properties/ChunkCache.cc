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
pyre::h5::py::properties::chunkCacheClass(py::module & m)
{
    // register the class of the chunk cache description
    py::class_<ChunkCache>(
        // in scope
        m,
        // class name
        "ChunkCache",
        // docstring
        "the cache a dataset is read and written through");

    // all done
    return;
}


// the chunk cache description
void
pyre::h5::py::properties::chunkCache()
{
    // the class, registered by {chunkCacheClass}
    auto cls = py::class_<ChunkCache>(py::type::of<ChunkCache>());

    // constructor; every field must be named, so a call site says what its numbers mean
    cls.def(
        // the implementation
        py::init<std::size_t, std::size_t, double>(),
        // the signature
        "slots"_a, "bytes"_a, "preemption"_a,
        // the docstring
        "describe a chunk cache with {slots} index entries, a budget of {bytes}, and the "
        "given {preemption} policy");

    // the size of the index
    cls.def_readwrite(
        // the name
        "slots",
        // the field
        &ChunkCache::slots,
        // the docstring
        "the number of slots in the hash table that indexes my cached chunks");

    // the memory budget
    cls.def_readwrite(
        // the name
        "bytes",
        // the field
        &ChunkCache::bytes,
        // the docstring
        "how much memory i may hold");

    // the eviction policy
    cls.def_readwrite(
        // the name
        "preemption",
        // the field
        &ChunkCache::preemption,
        // the docstring
        "how strongly to favor evicting a chunk that has been fully read or written");

    // rendering
    cls.def(
        // the name
        "__str__",
        // the implementation
        [](const ChunkCache & self) -> string_t {
            // say what each number is
            return "chunk cache: " + std::to_string(self.slots) + " slots, "
                 + std::to_string(self.bytes) + " bytes, preemption "
                 + std::to_string(self.preemption);
        },
        // the docstring
        "a human readable rendering");

    // all done
    return;
}


// end of file
