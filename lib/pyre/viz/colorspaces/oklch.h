// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include <cmath>


// the OKLCH to RGB conversion kernel
// see: https://oklch.com
auto
pyre::viz::colorspaces::oklch(float lightness, float chroma, float hue) -> viz::rgb_t
{
    // pi, once again
    constexpr float pi = 3.14159265358979323846f;

    // function to clamp a value to [0,1]
    auto clamp = [](float x) -> float {
        return std::max(0.0f, std::min(1.0f, x));
    };

    // the gamma encoder
    auto gamma = [](float x) -> float {
        x = x < 0.f ? 0.f : x;
        if (x <= 0.0031308f) {
            return 12.92f * x;
        }
        return 1.055f * std::pow(x, 1.f / 2.4f) - 0.055f;
    };

    float h = hue * pi / 180.f;
    float a = chroma * std::cos(h);
    float b = chroma * std::sin(h);

    // OKLab -> LMS cube roots
    float _l = lightness + 0.3963377774f * a + 0.2158037573f * b;
    float _m = lightness - 0.1055613458f * a - 0.0638541728f * b;
    float _s = lightness - 0.0894841775f * a - 1.2914855480f * b;

    // cube
    float l = _l * _l * _l;
    float m = _m * _m * _m;
    float s = _s * _s * _s;

    // LMS -> linear RGB
    float red = +4.0767416621f * l - 3.3077115913f * m + 0.2309699292f * s;
    float green = -1.2684380046f * l + 2.6097574011f * m - 0.3413193965f * s;
    float blue = -0.0041960863f * l - 0.7034186147f * m + 1.7076147010f * s;
    // gamma encode
    red = clamp(gamma(red));
    green = clamp(gamma(green));
    blue = clamp(gamma(blue));

    return { red, green, blue };
}


// end of file
