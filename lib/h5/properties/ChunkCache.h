// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the properties of the chunk cache of a dataset
class pyre::h5::properties::ChunkCache {
    // types
public:
    // me
    using self_type = ChunkCache;

    // metamethods
public:
    // make a chunk cache description
    ChunkCache(std::size_t slots, std::size_t bytes, double preemption);
    // the full set of special members
    ChunkCache(const ChunkCache &) = default;
    ChunkCache(ChunkCache &&) noexcept = default;
    ChunkCache & operator=(const ChunkCache &) = default;
    ChunkCache & operator=(ChunkCache &&) noexcept = default;
    ~ChunkCache() = default;

    // data
public:
    // the number of slots in the hash table that indexes cached chunks; hdf5 wants a prime
    // number comfortably larger than the number of chunks that fit in the cache
    std::size_t slots;
    // how much memory the cache may hold
    std::size_t bytes;
    // how strongly to favor evicting a chunk that has been fully read or written, from 0
    // for never to 1 for always
    double preemption;
};


// the inline definitions
#include "ChunkCache.icc"


// end of file
