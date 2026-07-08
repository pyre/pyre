// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {string_t} type, and the {esc} constant this serializer relies on
#include "../forward.h"


// serialize a 16-color palette {code} as an ANSI escape sequence
inline auto
pyre::chroma::ansi::csi3(int code, bool bright) -> string_t
{
    // start the control sequence with the escape character
    string_t seq { esc };
    // choose the bright or the normal weight
    seq += bright ? "[1;" : "[0;";
    // append the color code and close the sequence
    seq += std::to_string(code) + "m";
    // hand it back
    return seq;
}


// end of file
