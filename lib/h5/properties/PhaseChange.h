// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the thresholds at which storage switches representation
// hdf5 keeps a few items inline and spills to an indexed structure once there are many;
// the gap between the two bounds is what keeps it from thrashing at the boundary
class pyre::h5::properties::PhaseChange {
    // types
public:
    // me
    using self_type = PhaseChange;

    // metamethods
public:
    // describe the thresholds at which storage switches representation
    PhaseChange(unsigned int maxCompact, unsigned int minDense);
    // the full set of special members
    PhaseChange(const PhaseChange &) = default;
    PhaseChange(PhaseChange &&) noexcept = default;
    PhaseChange & operator=(const PhaseChange &) = default;
    PhaseChange & operator=(PhaseChange &&) noexcept = default;
    ~PhaseChange() = default;

    // data
public:
    // the count above which storage becomes indexed
    unsigned int maxCompact;
    // the count below which it goes back to being inline
    unsigned int minDense;
};


// the inline definitions
#include "PhaseChange.icc"


// end of file
