// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// what the page buffer of a file has seen since it was opened, or since its tally was last reset
// every count comes as a pair: the first entry is about metadata, the second about raw data, the
// two kinds of page the buffer keeps apart
class pyre::h5::PageBufferStats {
    // types
public:
    // me
    using self_type = PageBufferStats;
    // a pair of counts, metadata first, raw data second
    using counts_type = std::array<unsigned int, 2>;

    // metamethods
public:
    // record a tally
    PageBufferStats(
        counts_type accesses, counts_type hits, counts_type misses, counts_type evictions,
        counts_type bypasses);
    // the full set of special members
    PageBufferStats(const PageBufferStats &) = default;
    PageBufferStats(PageBufferStats &&) noexcept = default;
    PageBufferStats & operator=(const PageBufferStats &) = default;
    PageBufferStats & operator=(PageBufferStats &&) noexcept = default;
    ~PageBufferStats() = default;

    // data
public:
    // the requests the buffer was asked to serve
    counts_type accesses;
    // the ones it served from a page it already held
    counts_type hits;
    // the ones that sent it to the file for a page
    counts_type misses;
    // the pages it let go of to make room
    counts_type evictions;
    // the requests too large for a page, which went to the file without it
    counts_type bypasses;
};


// the inline definitions
#include "PageBufferStats.icc"


// end of file
