// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// STL
#include <cassert>
#include <limits>
#include <vector>
// support
#include <pyre/viz.h>


// type aliases
using bmp_t = pyre::viz::iterators::codecs::bmp_t;
using rgb_t = bmp_t::rgb_type;
using color_t = pyre::viz::color_t;
using source_t = std::vector<double>::const_iterator;
using colormap_t = pyre::viz::iterators::colormaps::rgb_t<source_t, source_t, source_t>;

// encode colors whose channels fall outside the unit interval, and check that every one lands on
// the nearest end of the byte range, with a value that is not a number counted as zero, both when
// the colors arrive as triplets and when the {rgb} colormap assembles them from three channels
int
main(int argc, char * argv[])
{
    // a square tile whose lines need no padding
    const int height = 16;
    const int width = 16;
    // the number of pixels
    const int pixels = height * width;
    // a value that is not a number
    const auto nan = std::numeric_limits<color_t>::quiet_NaN();

    // the colors: too bright, too dark, and not a number
    std::vector<rgb_t> colors(pixels, rgb_t { 22.5, -3.0, nan });
    // make a bitmap
    bmp_t bmp(height, width);
    // encode
    auto start = colors.cbegin();
    auto img = bmp.encode(start);

    // the size of a header
    const int header = 54;
    // go through the pixels
    for (int pixel = 0; pixel < pixels; ++pixel) {
        // the blue byte is not a number, so it is dark
        assert(img[header + 3 * pixel + 0] == 0x00);
        // the green byte is below the interval, so it is dark
        assert(img[header + 3 * pixel + 1] == 0x00);
        // and the red byte is above it, so it is as bright as a byte can be
        assert(img[header + 3 * pixel + 2] == 0xff);
    }

    // the same values, as three channels
    std::vector<double> red(pixels, 22.5);
    std::vector<double> green(pixels, -3.0);
    std::vector<double> blue(pixels, nan);
    // assembled by the colormap
    colormap_t colormap(red.cbegin(), green.cbegin(), blue.cbegin());
    // land in the unit cube
    assert((*colormap == rgb_t { 1, 0, 0 }));

    // all done
    return 0;
}


// end of file
