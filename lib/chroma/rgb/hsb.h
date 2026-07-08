// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {rgb_t} type, and the external math this kernel relies on
#include "../forward.h"


// the {hsb/hsv} to {rgb} conversion kernel
// see the wikipedia article at {https://en.wikipedia.org/wiki/HSL_and_HSV#HSB_to_RGB}
// N.B.: {hue} in [-π, π] radians, {saturation} and {brightness} in [0, 1]
inline auto
pyre::chroma::rgb::hsb(double hue, double saturation, double brightness) -> rgb_t
{
    // the reference formula is written in degrees, so convert the hue
    hue *= 180 / M_PI;
    // evaluate one channel, chosen by its phase offset {n} on the color wheel
    auto f = [=](double n) -> color_t {
        // locate this channel within the repeating six-step hue cycle
        auto k = std::fmod((n + hue / 60), 6);
        // the saturation carves a triangular notch out of full brightness
        auto a = saturation * std::max(0.0, std::min({ k, 4 - k, 1.0 }));
        // scale brightness down by that notch
        auto v = brightness * (1 - a);
        // hand back the channel value
        return v;
    };

    // sample the kernel at the red, green, and blue offsets and pack the triplet
    return { f(5), f(3), f(1) };
}


// end of file
