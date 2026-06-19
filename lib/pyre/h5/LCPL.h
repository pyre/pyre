// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "PropList.h"


// a link creation property list
class pyre::h5::LCPL : public pyre::h5::PropList {
    // metamethods
public:
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
#if H5_VERSION_GE(1, 12, 0)
    // whether missing intermediate groups are created on demand
    auto createIntermediateGroup() const -> bool;
    // set whether missing intermediate groups are created on demand
    auto setCreateIntermediateGroup(bool create) -> void;
#endif
    // the string character encoding
    auto charEncoding() const -> H5T_cset_t;
    // set the string character encoding
    auto setCharEncoding(H5T_cset_t encoding) -> void;

    // implementation details
protected:
    // adopt an existing raw handle
    explicit LCPL(id_type id);
};


// end of file
