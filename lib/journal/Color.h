// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Color_h)
#define pyre_journal_Color_h


// information about the location of the channel invocation
class pyre::journal::Color {
    // types
public:
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
#define pyre_journal_Color_icc
#include "Color.icc"
#undef pyre_journal_Color_icc


#endif

// end of file
