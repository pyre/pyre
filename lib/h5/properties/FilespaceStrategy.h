// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// how a file manages the space its deleted objects leave behind
// a threshold of zero puts every free block on the list, however small
class pyre::h5::properties::FilespaceStrategy {
    // types
public:
    // me
    using self_type = FilespaceStrategy;

    // metamethods
public:
    // describe how a file manages the space its deleted objects leave behind
    FilespaceStrategy(H5F_fspace_strategy_t strategy, bool persist, hsize_t threshold);
    // the full set of special members
    FilespaceStrategy(const FilespaceStrategy &) = default;
    FilespaceStrategy(FilespaceStrategy &&) noexcept = default;
    FilespaceStrategy & operator=(const FilespaceStrategy &) = default;
    FilespaceStrategy & operator=(FilespaceStrategy &&) noexcept = default;
    ~FilespaceStrategy() = default;

    // data
public:
    // how free space is tracked
    H5F_fspace_strategy_t strategy;
    // whether the free space survives closing the file
    bool persist;
    // the smallest block worth tracking
    hsize_t threshold;
};


// the inline definitions
#include "FilespaceStrategy.icc"


// end of file
