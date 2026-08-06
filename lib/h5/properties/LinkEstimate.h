// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// what a group expects to hold, so its object header is sized for it
// a guess only: hdf5 grows the header if the group outgrows it
class pyre::h5::properties::LinkEstimate {
    // types
public:
    // me
    using self_type = LinkEstimate;

    // metamethods
public:
    // describe what a group expects to hold, so its object header is sized for it
    LinkEstimate(unsigned int links, unsigned int nameLength);
    // the full set of special members
    LinkEstimate(const LinkEstimate &) = default;
    LinkEstimate(LinkEstimate &&) noexcept = default;
    LinkEstimate & operator=(const LinkEstimate &) = default;
    LinkEstimate & operator=(LinkEstimate &&) noexcept = default;
    ~LinkEstimate() = default;

    // data
public:
    // how many members the group expects
    unsigned int links;
    // how long their names run, on average
    unsigned int nameLength;
};


// the inline definitions
#include "LinkEstimate.icc"


// end of file
