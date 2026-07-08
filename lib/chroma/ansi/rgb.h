// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {rgb_t}/{string_t} types, and the {esc} constant this serializer relies on
#include "../forward.h"


// serialize an {rgb} triplet as a 24-bit truecolor ANSI escape sequence
inline auto
pyre::chroma::ansi::rgb(const rgb_t & color, bool foreground) -> string_t
{
    // scale a unit channel to a byte in [0, 255], clamping anything out of gamut
    auto byte = [](color_t channel) -> int {
        // hold the channel inside the unit interval
        auto clamped = std::max(color_t(0), std::min(color_t(1), channel));
        // then scale to a byte and round to the nearest integer
        return static_cast<int>(clamped * 255 + 0.5f);
    };

    // start the control sequence with the escape character
    string_t seq { esc };
    // select the foreground or background plane, then the truecolor introducer
    seq += foreground ? "[38;2;" : "[48;2;";
    // append the red channel
    seq += std::to_string(byte(color.red)) + ";";
    // then the green channel
    seq += std::to_string(byte(color.green)) + ";";
    // then the blue channel
    seq += std::to_string(byte(color.blue));
    // close the sequence
    seq += "m";
    // hand it back
    return seq;
}


// end of file
