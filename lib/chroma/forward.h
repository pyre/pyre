// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the external dependencies the converters rely on
#include "external.h"


// set up the namespace and establish the fundamental color types
namespace pyre::chroma {
    // a single color channel is a float living in the unit interval [0, 1]
    using color_t = float;

    // an {r,g,b} triplet is our canonical device-independent representation of a color
    struct rgb_t {
        // the red channel, in [0, 1]
        color_t red;
        // the green channel, in [0, 1]
        color_t green;
        // the blue channel, in [0, 1]
        color_t blue;

        // two colors are identical iff their three channels agree
        auto operator==(const rgb_t & other) const -> bool
        {
            // compare the channels one by one
            return red == other.red && green == other.green && blue == other.blue;
        }
    };

    // the converters that assemble an {rgb} triplet from another color representation
    // the enclosing namespace names the destination color space; each function names its source
    namespace rgb {
        // from {hsl}: {hue} in [-π, π] radians, {saturation} and {luminosity} in [0, 1]
        inline auto hsl(double hue, double saturation, double luminosity) -> rgb_t;
        // from {hsb/hsv}: {hue} in [-π, π] radians, {saturation} and {brightness} in [0, 1]
        inline auto hsb(double hue, double saturation, double brightness) -> rgb_t;
        // from {hl}: a complex-display map of {hue} and {luminosity} with a mixing {threshold}
        inline auto hl(double hue, double luminosity, double threshold = 0.4) -> rgb_t;
        // from {oklch}: perceptual {lightness} and {chromaLevel} with {hue} in degrees
        inline auto oklch(float lightness, float chromaLevel, float hue) -> rgb_t;
    } // namespace rgb
} // namespace pyre::chroma


// end of file
