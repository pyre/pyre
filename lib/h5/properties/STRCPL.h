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


// the properties shared by everything that creates a name
// hdf5 makes this the parent of the link and attribute creation lists, since both of them
// lay down a string, and the character set that string is recorded in is the one decision
// they have in common
class pyre::h5::properties::STRCPL : public pyre::h5::properties::List {
    // metamethods
public:
    // me
    using self_type = STRCPL;
    // my superclass
    using super_type = pyre::h5::properties::List;
    // the full set of special members; there is no public default constructor because a
    // string creation property is always part of a concrete list
    STRCPL(const STRCPL &) = default;
    STRCPL(STRCPL &&) noexcept = default;
    STRCPL & operator=(const STRCPL &) = default;
    STRCPL & operator=(STRCPL &&) noexcept = default;
    ~STRCPL() override = default;

    // interface
public:
    // the character set the names i create are recorded in
    auto charEncoding() const -> H5T_cset_t;
    // set the character set
    auto setCharEncoding(H5T_cset_t encoding) -> void;

    // implementation details
protected:
    // adopt an existing raw handle; for derived lists to pass a freshly created one
    explicit STRCPL(id_type id);
};


// end of file
