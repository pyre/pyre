// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "OCPL.h"


// a group creation property list
class pyre::h5::properties::GCPL : public pyre::h5::properties::OCPL {
    // metamethods
public:
    // me
    using self_type = GCPL;
    // my superclass
    using super_type = pyre::h5::properties::OCPL;
    // make a fresh group creation property list
    GCPL();
    // the full set of special members
    GCPL(const GCPL &) = default;
    GCPL(GCPL &&) noexcept = default;
    GCPL & operator=(const GCPL &) = default;
    GCPL & operator=(GCPL &&) noexcept = default;
    ~GCPL() override = default;

    // static interface
public:
    // the shared default group creation property list
    static auto theDefault() -> const GCPL &;

    // interface
public:
    // the thresholds at which link storage switches representation, as
    // (max compact, min dense)
    auto linkPhaseChange() const -> std::tuple<unsigned int, unsigned int>;
    // set the link storage thresholds
    auto setLinkPhaseChange(unsigned int maxCompact, unsigned int minDense) -> void;

    // whether the order in which links were created is tracked and indexed; without this,
    // members come back in the order the library finds convenient rather than the order
    // they were laid down
    auto linkCreationOrder() const -> CreationOrder;
    // set the link creation order flags
    auto setLinkCreationOrder(CreationOrder flags) -> void;

    // the expectations that size my object header, as (number of links, name length)
    auto estimatedLinkInfo() const -> std::tuple<unsigned int, unsigned int>;
    // set the expected number of links and their average name length
    auto setEstimatedLinkInfo(unsigned int links, unsigned int nameLength) -> void;

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit GCPL(id_type id);
};


// end of file
