// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the file format versions hdf5 may use
// asking for a recent format buys newer features and narrows who can read the result
class pyre::h5::properties::VersionBounds {
    // types
public:
    // me
    using self_type = VersionBounds;

    // metamethods
public:
    // describe the file format versions hdf5 may use
    VersionBounds(H5F_libver_t low, H5F_libver_t high);
    // the full set of special members
    VersionBounds(const VersionBounds &) = default;
    VersionBounds(VersionBounds &&) noexcept = default;
    VersionBounds & operator=(const VersionBounds &) = default;
    VersionBounds & operator=(VersionBounds &&) noexcept = default;
    ~VersionBounds() = default;

    // data
public:
    // the oldest format i may write
    H5F_libver_t low;
    // the newest format i may write
    H5F_libver_t high;
};


// the inline definitions
#include "VersionBounds.icc"


// end of file
