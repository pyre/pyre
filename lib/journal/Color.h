// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// information about the location of the channel invocation
class pyre::journal::Color {
    // types
public:
    // me
    using self_type = Color;

    // {Color} remembers a {color_t} level
    using color_type = colorrep_t;

    // metamethods
public:
    // constructor
    inline explicit Color(color_type);

    // interface
public:
    // accessors
    inline auto color() const -> color_type;

    // data
private:
    const color_type _color;
};


// get the inline definitions
#include "Color.icc"


// end of file
