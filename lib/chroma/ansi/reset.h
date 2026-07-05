// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {string_t} type, and the {esc} constant this serializer relies on
#include "../forward.h"


// the ANSI reset sequence that returns the terminal to its default attributes
inline auto
pyre::chroma::ansi::reset() -> string_t
{
    // start the control sequence with the escape character
    string_t seq { esc };
    // close it with the reset code and hand it back
    return seq + "[0m";
}


// end of file
