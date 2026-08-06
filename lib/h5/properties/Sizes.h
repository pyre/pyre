// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the widths hdf5 records positions and lengths in
// these are fixed when a file is made and cannot be revised afterwards
class pyre::h5::properties::Sizes {
    // types
public:
    // me
    using self_type = Sizes;

    // metamethods
public:
    // describe the widths hdf5 records positions and lengths in
    Sizes(std::size_t offsets, std::size_t lengths);
    // the full set of special members
    Sizes(const Sizes &) = default;
    Sizes(Sizes &&) noexcept = default;
    Sizes & operator=(const Sizes &) = default;
    Sizes & operator=(Sizes &&) noexcept = default;
    ~Sizes() = default;

    // data
public:
    // how many bytes a position in the file takes
    std::size_t offsets;
    // how many bytes a length takes
    std::size_t lengths;
};


// the inline definitions
#include "Sizes.icc"


// end of file
