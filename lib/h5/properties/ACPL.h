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


// an attribute creation property list
// everything it governs is inherited: an attribute is a name and a value, and the only
// creation decision hdf5 offers is the character set the name is recorded in
class pyre::h5::properties::ACPL : public pyre::h5::properties::STRCPL {
    // metamethods
public:
    // me
    using self_type = ACPL;
    // my superclass
    using super_type = pyre::h5::properties::STRCPL;
    // make a fresh attribute creation property list
    ACPL();
    // the full set of special members
    ACPL(const ACPL &) = default;
    ACPL(ACPL &&) noexcept = default;
    ACPL & operator=(const ACPL &) = default;
    ACPL & operator=(ACPL &&) noexcept = default;
    ~ACPL() override = default;

    // static interface
public:
    // the shared default attribute creation property list
    static auto theDefault() -> const ACPL &;

    // low-level interface
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit ACPL(id_type id);
};


// end of file
