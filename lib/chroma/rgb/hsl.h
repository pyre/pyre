// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {rgb_t} type, and the external math this kernel relies on
#include "../forward.h"


// the {hsl} to {rgb} conversion kernel
// see the wikipedia article at {https://en.wikipedia.org/wiki/HSL_and_HSV#HSL_to_RGB}
// N.B.: {hue} in [-π, π] radians, {saturation} and {luminosity} in [0, 1]
inline auto
pyre::chroma::rgb::hsl(double hue, double saturation, double luminosity) -> rgb_t
{
    // the reference formula is written in degrees, so convert the hue
    hue *= 180 / M_PI;
    // the chroma amplitude scales each channel away from the gray at this luminosity
    auto a = saturation * std::min(luminosity, 1 - luminosity);
    // evaluate one channel, chosen by its phase offset {n} on the color wheel
    auto f = [=](double n) -> color_t {
        // locate this channel within the repeating twelve-step hue cycle
        auto k = std::fmod((n + hue / 30), 12);
        // ride the triangle wave down from luminosity by the chroma amplitude
        auto v = luminosity - a * std::max(-1.0, std::min({ k - 3, 9 - k, 1.0 }));
        // hand back the channel value
        return v;
    };

    // sample the kernel at the red, green, and blue offsets and pack the triplet
    return { f(0), f(8), f(4) };
}


// end of file
