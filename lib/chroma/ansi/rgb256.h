// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {rgb_t}/{string_t} types, and the {esc} constant this serializer relies on
#include "../forward.h"


// serialize an {rgb} triplet into the 6×6×6 color cube of the 256-color palette
inline auto
pyre::chroma::ansi::rgb256(const rgb_t & color, bool foreground) -> string_t
{
    // scale a unit channel onto the six-level axis [0, 5] of the color cube
    auto level = [](color_t channel) -> int {
        // hold the channel inside the unit interval
        auto clamped = std::max(color_t(0), std::min(color_t(1), channel));
        // then scale to a cube axis and round to the nearest level
        return static_cast<int>(clamped * 5 + 0.5f);
    };

    // the color cube occupies indices 16–231 of the 256-color palette, packed as
    // 16 + 36·red + 6·green + blue with each channel on the [0, 5] axis
    int index = 16 + 36 * level(color.red) + 6 * level(color.green) + level(color.blue);
    // start the control sequence with the escape character
    string_t seq { esc };
    // select the foreground or background plane, then the indexed-color introducer
    seq += foreground ? "[38;5;" : "[48;5;";
    // append the cube index and close the sequence
    seq += std::to_string(index) + "m";
    // hand it back
    return seq;
}


// end of file
