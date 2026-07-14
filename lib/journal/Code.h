// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// attach a code to a message
class pyre::journal::Code {
    // types
public:
    // codes are strings
    using code_type = string_t;

    // metamethods
public:
    // constructor
    inline explicit Code(code_type);

    // interface
public:
    // accessors
    inline auto code() const -> code_type;

    // data
private:
    const code_type _code;
};


// get the inline definitions
#include "Code.icc"


// end of file
