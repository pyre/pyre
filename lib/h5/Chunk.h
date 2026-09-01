// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// one chunk of a chunked dataset, as it exists in the file
// a chunk that was never written has no entry in the chunk table and therefore no instance of
// this: the dataset reports its absence rather than handing back a hollow record, so every
// chunk described here is one that can actually be read
class pyre::h5::Chunk {
    // types
public:
    // me
    using self_type = Chunk;

    // metamethods
public:
    // describe a chunk that exists in the file
    Chunk(index_t origin, unsigned int filterMask, haddr_t address, hsize_t bytes);
    // the full set of special members
    Chunk(const Chunk &) = default;
    Chunk(Chunk &&) noexcept = default;
    Chunk & operator=(const Chunk &) = default;
    Chunk & operator=(Chunk &&) noexcept = default;
    ~Chunk() = default;

    // data
public:
    // where my first cell sits in the dataset's index space; always a multiple of the chunk
    // shape, since chunks tile the extent from the origin outwards
    index_t origin;
    // which stages of the dataset's filter pipeline were skipped when i was written; a set
    // bit means that filter did not run on me, so i am not necessarily shaped like my
    // siblings and anyone reading me raw has to honor it
    unsigned int filterMask;
    // where i live in the file
    haddr_t address;
    // how much room i take up there, after the pipeline had its way with me; this is the
    // compressed size, not the size of the cells i decode into
    hsize_t bytes;
};


// the inline definitions
#include "Chunk.icc"


// end of file
