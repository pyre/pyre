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
    // ANSI escape sequences are assembled as strings
    using string_t = std::string;

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

    // the serializers that render a color as an ANSI escape sequence
    // the enclosing namespace names the destination representation; each function names its source
    namespace ansi {
        // the escape character that introduces every control sequence
        inline constexpr char esc = '\x1b';

        // the reset sequence returns the terminal to its default attributes
        inline auto reset() -> string_t;
        // from an {rgb} triplet: a 24-bit truecolor escape sequence
        inline auto rgb(const rgb_t & color, bool foreground = true) -> string_t;
        // from an {rgb} triplet: the nearest color in the 216-color cube
        inline auto rgb256(const rgb_t & color, bool foreground = true) -> string_t;
        // from a gray {level} in [0, 1]: the nearest step on the 24-step grayscale ramp
        inline auto gray(color_t level, bool foreground = true) -> string_t;
    } // namespace ansi
} // namespace pyre::chroma


// end of file
