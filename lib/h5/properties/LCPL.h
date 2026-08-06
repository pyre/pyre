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
#include "STRCPL.h"


// a link creation property list
class pyre::h5::properties::LCPL : public pyre::h5::properties::STRCPL {
    // metamethods
public:
    // me
    using self_type = LCPL;
    // my superclass
    using super_type = pyre::h5::properties::STRCPL;
    // make a fresh link creation property list
    LCPL();
    // the full set of special members
    LCPL(const LCPL &) = default;
    LCPL(LCPL &&) noexcept = default;
    LCPL & operator=(const LCPL &) = default;
    LCPL & operator=(LCPL &&) noexcept = default;
    ~LCPL() override = default;

    // static interface
public:
    // the shared default link creation property list
    static auto theDefault() -> const LCPL &;

    // interface
public:
    // whether missing intermediate groups are created on demand
    auto intermediateGroupCreation() const -> bool;
    // set whether missing intermediate groups are created on demand
    auto intermediateGroupCreation(bool create) -> void;

    // implementation details
protected:
    // adopt an existing raw handle
    explicit LCPL(id_type id);
};


// end of file
