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
#include "List.h"


// a link access property list
class pyre::h5::properties::LAPL : public pyre::h5::properties::List {
    // metamethods
public:
    // me
    using self_type = LAPL;
    // my superclass
    using super_type = pyre::h5::properties::List;
    // make a fresh link access property list
    LAPL();
    // the full set of special members
    LAPL(const LAPL &) = default;
    LAPL(LAPL &&) noexcept = default;
    LAPL & operator=(const LAPL &) = default;
    LAPL & operator=(LAPL &&) noexcept = default;
    ~LAPL() override = default;

    // static interface
public:
    // the shared default link access property list
    static auto theDefault() -> const LAPL &;

    // interface
public:
    // the number of allowed link traversals
    auto numLinks() const -> std::size_t;
    // set the number of allowed link traversals
    auto setNumLinks(std::size_t links) -> void;

    // the prefix prepended to the filename an external link names; this is how a product
    // whose external targets have moved is read without editing the links themselves
    auto externalPrefix() const -> string_t;
    // set the prefix prepended to external link filenames
    auto setExternalPrefix(const string_t & prefix) -> void;

    // implementation details
protected:
    // adopt an existing raw handle
    explicit LAPL(id_type id);
};


// end of file
