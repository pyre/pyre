// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "DAPL.h"
// the reporting of library refusals
#include "../diagnostics.h"


// make a fresh dataset access property list
pyre::h5::properties::DAPL::DAPL() : List(H5Pcreate(H5P_DATASET_ACCESS))
{
    // if the library refused to make it
    if (!valid()) {
        // complain
        complain("pyre.h5.dapl", "creating a dataset access property list");
    }
}


// adopt an existing raw handle
pyre::h5::properties::DAPL::DAPL(id_type id) : List(id) {}


// the shared default dataset access property list
auto
pyre::h5::properties::DAPL::theDefault() -> const DAPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const DAPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// the chunk cache my datasets are read and written through
auto
pyre::h5::properties::DAPL::chunkCache() const -> ChunkCache
{
    // make room for the answer
    std::size_t slots = 0;
    std::size_t bytes = 0;
    double preemption = 0;
    // ask the library
    if (H5Pget_chunk_cache(id(), &slots, &bytes, &preemption) < 0) {
        // complain if it refused
        complain("pyre.h5.dapl", "retrieving the chunk cache settings");
        // and report an empty cache
        return ChunkCache(0, 0, 0);
    }
    // otherwise, hand it back as something that says what each number is
    return ChunkCache(slots, bytes, preemption);
}


// set the chunk cache my datasets are read and written through
auto
pyre::h5::properties::DAPL::chunkCache(const ChunkCache & cache) -> void
{
    // take the description apart for the library
    if (H5Pset_chunk_cache(id(), cache.slots, cache.bytes, cache.preemption) < 0) {
        // and complain if it refused
        complain("pyre.h5.dapl", "setting the chunk cache");
    }
    // all done
    return;
}


// end of file
