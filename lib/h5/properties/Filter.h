// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// one stage of the pipeline a dataset's cells pass through
// filters are applied in the order they were added, so a pipeline is a sequence of these
class pyre::h5::properties::Filter {
    // types
public:
    // me
    using self_type = Filter;

    // metamethods
public:
    // describe one stage of the pipeline a dataset's cells pass through
    Filter(H5Z_filter_t id, string_t name, unsigned int flags, unsigned int configuration);
    // the full set of special members
    Filter(const Filter &) = default;
    Filter(Filter &&) noexcept = default;
    Filter & operator=(const Filter &) = default;
    Filter & operator=(Filter &&) noexcept = default;
    ~Filter() = default;

    // data
public:
    // which filter this is
    H5Z_filter_t id;
    // what the library calls it
    string_t name;
    // how the library treats a failure of this stage
    unsigned int flags;
    // whether the filter can encode, decode, or both
    unsigned int configuration;
};


// the inline definitions
#include "Filter.icc"


// end of file
