// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// the namespace, the {rgb_t} type, and the external math this kernel relies on
#include "../forward.h"


// the {oklch} to {rgb} conversion kernel
// see the reference implementation at {https://oklch.com}
// N.B.: {hue} in degrees, {lightness} and {chromaLevel} in [0, 1]
inline auto
pyre::chroma::rgb::oklch(float lightness, float chromaLevel, float hue) -> rgb_t
{
    // π, expressed in single precision for this all-float kernel
    constexpr float pi = 3.14159265358979323846f;

    // clamp a channel back into the displayable unit interval
    auto clamp = [](float x) -> float {
        // never below zero, never above one
        return std::max(0.0f, std::min(1.0f, x));
    };

    // the sRGB gamma encoder that maps linear light to display values
    auto gamma = [](float x) -> float {
        // negative light is meaningless, so floor it at zero
        x = x < 0.f ? 0.f : x;
        // the toe of the curve is a straight line
        if (x <= 0.0031308f) {
            // with this slope
            return 12.92f * x;
        }
        // the rest follows the power-law shoulder
        return 1.055f * std::pow(x, 1.f / 2.4f) - 0.055f;
    };

    // turn the polar {chroma, hue} into the rectangular {a, b} axes of OKLab
    float h = hue * pi / 180.f;
    // the green-red axis
    float a = chromaLevel * std::cos(h);
    // the blue-yellow axis
    float b = chromaLevel * std::sin(h);

    // recover the cube roots of the LMS cone responses from OKLab
    float _l = lightness + 0.3963377774f * a + 0.2158037573f * b;
    float _m = lightness - 0.1055613458f * a - 0.0638541728f * b;
    float _s = lightness - 0.0894841775f * a - 1.2914855480f * b;

    // cube them to recover the cone responses themselves
    float l = _l * _l * _l;
    float m = _m * _m * _m;
    float s = _s * _s * _s;

    // convert the cone responses to linear {rgb}
    float red = +4.0767416621f * l - 3.3077115913f * m + 0.2309699292f * s;
    float green = -1.2684380046f * l + 2.6097574011f * m - 0.3413193965f * s;
    float blue = -0.0041960863f * l - 0.7034186147f * m + 1.7076147010f * s;

    // gamma-encode and clamp the red channel for display
    red = clamp(gamma(red));
    // likewise for green
    green = clamp(gamma(green));
    // and blue
    blue = clamp(gamma(blue));

    // pack the displayable triplet
    return { red, green, blue };
}


// end of file
