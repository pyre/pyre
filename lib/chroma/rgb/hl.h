// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {rgb_t} type, and the external math this kernel relies on
#include "../forward.h"


// the {hl} to {rgb} conversion kernel
// maps {hue} and {luminosity} to {rgb} with a colormap designed for displaying complex values
// [zebker@stanford.edu, private communication]
inline auto
pyre::chroma::rgb::hl(double hue, double luminosity, double threshold) -> rgb_t
{
    // one third of the way around the color wheel
    const auto angle = 2 * M_PI / 3;

    // fold negative hues into the upper half so the wheel is single valued
    if (hue < 0) {
        // by adding a full turn
        hue += 2 * M_PI;
    }

    // choose the 120° region of the wheel that this hue occupies
    int axis = hue / angle;
    // and how far it has advanced into that region, as a fraction in [0, 1]
    auto mix = std::fmod(hue, angle) / angle;

    // the color dual to the dominant region shows at the requested luminosity
    color_t dual = luminosity;
    // the color at the low edge of the region fades toward the {threshold} floor
    color_t low = luminosity * (threshold + (1 - threshold) * mix);
    // the color at the high edge fades the opposite way
    color_t high = luminosity * (threshold + (1 - threshold) * (1 - mix));
    // gather the three candidate levels
    color_t wheel[] = { low, high, dual };
    // rotate them into {r,g,b} by the dominant region and pack the triplet
    return { wheel[(3 - axis) % 3], wheel[(4 - axis) % 3], wheel[(5 - axis) % 3] };
}


// end of file
