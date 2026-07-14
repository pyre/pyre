// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// notes are channel manipulators that decorate channels with metadata
class pyre::journal::Note {
    // types
public:
    // me
    using self_type = Note;
    // my parts
    using key_type = key_t;
    using value_type = value_t;

    // metamethods
public:
    // constructor
    inline Note(key_type, value_type);

    // interface
public:
    inline auto key() const -> const key_type &;
    inline auto value() const -> const value_type &;

    // data
private:
    key_type _key;
    value_type _value;
};


// get the inline definitions
#include "Note.icc"


// end of file
