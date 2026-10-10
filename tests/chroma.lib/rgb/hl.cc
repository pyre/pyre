// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <limits>
// get the chroma interface
#include <pyre/chroma.h>


// bring the color type into scope
using rgb_t = pyre::chroma::rgb_t;


// verify that the {hl} converter keeps its colors in the unit cube, whatever the luminosity
int
main(int argc, char * argv[])
{
    // pure black is what dark pixels become
    rgb_t black { 0, 0, 0 };
    // a value that is not a number
    const auto nan = std::numeric_limits<double>::quiet_NaN();

    // go around the wheel
    for (auto hue : { -M_PI, -M_PI / 2, 0.0, M_PI / 3, M_PI }) {
        // the color at full luminosity
        auto full = pyre::chroma::rgb::hl(hue, 1);
        // a luminosity above the unit interval saturates to the brightest color of its hue
        assert((pyre::chroma::rgb::hl(hue, 22.5) == full));
        // a luminosity below it is black
        assert((pyre::chroma::rgb::hl(hue, -3) == black));
        // and so is one that is not a number
        assert((pyre::chroma::rgb::hl(hue, nan) == black));
        // every channel of the brightest color stays in the unit interval
        auto [red, green, blue] = full;
        assert(red >= 0 && red <= 1);
        assert(green >= 0 && green <= 1);
        assert(blue >= 0 && blue <= 1);
    }

    // all done
    return 0;
}


// end of file
