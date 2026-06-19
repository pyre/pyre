// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "List.h"


// a dataset memory transfer property list
class pyre::h5::properties::DXPL : public pyre::h5::properties::List {
    // metamethods
public:
    // make a fresh dataset memory transfer property list
    DXPL();
    // make one that applies the given data transform {expression}
    explicit DXPL(const string_t & expression);
    // the full set of special members
    DXPL(const DXPL &) = default;
    DXPL(DXPL &&) noexcept = default;
    DXPL & operator=(const DXPL &) = default;
    DXPL & operator=(DXPL &&) noexcept = default;
    ~DXPL() override = default;

    // static interface
public:
    // the shared default dataset memory transfer property list
    static auto theDefault() -> const DXPL &;

    // implementation details
protected:
    // adopt an existing raw handle
    explicit DXPL(id_type id);
};


// end of file
