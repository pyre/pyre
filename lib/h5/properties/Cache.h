// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the caches a file reaches its data through
// hdf5 configures the metadata cache and the default chunk cache in one call; a dataset
// access property list overrides the chunk half for one dataset at a time
class pyre::h5::properties::Cache {
    // types
public:
    // me
    using self_type = Cache;

    // metamethods
public:
    // describe the caches a file reaches its data through
    Cache(int metadataElements, std::size_t slots, std::size_t bytes, double preemption);
    // the full set of special members
    Cache(const Cache &) = default;
    Cache(Cache &&) noexcept = default;
    Cache & operator=(const Cache &) = default;
    Cache & operator=(Cache &&) noexcept = default;
    ~Cache() = default;

    // data
public:
    // how many entries the metadata cache holds
    int metadataElements;
    // the number of slots in the hash table that indexes cached chunks
    std::size_t slots;
    // how much memory the chunk cache may hold
    std::size_t bytes;
    // how strongly to favor evicting a chunk that has been fully read or written
    double preemption;
};


// the inline definitions
#include "Cache.icc"


// end of file
