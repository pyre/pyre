// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the buffer a paged file gathers its pages in
// the two shares are percentages of {bytes}, and what is left over is available to either
class pyre::h5::properties::PageBuffer {
    // types
public:
    // me
    using self_type = PageBuffer;

    // metamethods
public:
    // describe the buffer a paged file gathers its pages in
    PageBuffer(std::size_t bytes, unsigned int metadata, unsigned int raw);
    // the full set of special members
    PageBuffer(const PageBuffer &) = default;
    PageBuffer(PageBuffer &&) noexcept = default;
    PageBuffer & operator=(const PageBuffer &) = default;
    PageBuffer & operator=(PageBuffer &&) noexcept = default;
    ~PageBuffer() = default;

    // data
public:
    // how much memory the buffer may hold
    std::size_t bytes;
    // the smallest share of the buffer reserved for metadata pages
    unsigned int metadata;
    // the smallest share reserved for raw data pages
    unsigned int raw;
};


// the inline definitions
#include "PageBuffer.icc"


// end of file
