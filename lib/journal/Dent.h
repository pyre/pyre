// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// information about the location of the channel invocation
class pyre::journal::Dent {
    // types
public:
    // {Dent} remembers a {dent_t} level
    using dent_type = dent_t;

    // metamethods
public:
    // constructor
    inline explicit Dent(dent_type);

    // interface
public:
    // accessors
    inline auto dent() const -> dent_type;

    // data
private:
    const dent_type _dent;
};


// get the inline definitions
#include "Dent.icc"


// end of file
