// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {string_t} type, and the {esc} constant this serializer relies on
#include "../forward.h"


// serialize a gray {level} in [0, 1] as the nearest step on the 24-step grayscale ramp
inline auto
pyre::chroma::ansi::gray(color_t level, bool foreground) -> string_t
{
    // hold the requested gray inside the unit interval
    auto clamped = std::max(color_t(0), std::min(color_t(1), level));
    // map it onto the 24-step ramp, which occupies indices 232 through 255
    int index = 232 + static_cast<int>(clamped * 23 + 0.5f);
    // start the control sequence with the escape character
    string_t seq { esc };
    // select the foreground or background plane, then the indexed-color introducer
    seq += foreground ? "[38;5;" : "[48;5;";
    // append the ramp index and close the sequence
    seq += std::to_string(index) + "m";
    // hand it back
    return seq;
}


// end of file
