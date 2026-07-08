// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the chroma interface
#include <pyre/chroma.h>


// bring the color type into scope
using rgb_t = pyre::chroma::rgb_t;


// verify that the {hsb} converter lands the primaries and the brightness axis where they belong
int
main(int argc, char * argv[])
{
    // pure black anchors the bottom of the brightness axis
    rgb_t black { 0, 0, 0 };
    // pure white sits at zero saturation and full brightness
    rgb_t white { 1, 1, 1 };
    // full red sits at hue zero
    rgb_t red { 1, 0, 0 };
    // full blue sits two thirds of the way around the wheel
    rgb_t blue { 0, 0, 1 };

    // red is hue 0 at full saturation and full brightness
    assert((pyre::chroma::rgb::hsb(0, 1, 1) == red));
    // blue is 4π/3 at full saturation and full brightness
    assert((pyre::chroma::rgb::hsb(4 * M_PI / 3, 1, 1) == blue));

    // anything at zero brightness is black, whatever the hue or saturation
    assert((pyre::chroma::rgb::hsb(0, 1, 0) == black));
    assert((pyre::chroma::rgb::hsb(2 * M_PI / 3, 1, 0) == black));

    // zero saturation at full brightness is white, whatever the hue
    assert((pyre::chroma::rgb::hsb(0, 0, 1) == white));
    assert((pyre::chroma::rgb::hsb(2 * M_PI / 3, 0, 1) == white));

    // all done
    return 0;
}


// end of file
