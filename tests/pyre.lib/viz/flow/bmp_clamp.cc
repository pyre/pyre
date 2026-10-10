// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
#include <limits>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>

// type aliases
using cell_t = float;
using packing_t = pyre::grid::canonical_t<2>;
using storage_t = pyre::memory::heap_t<cell_t>;
using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
using channel_t = pyre::flow::products::tile_t<grid_t>;
using image_t = pyre::viz::products::images::bmp_t;
using codec_t = pyre::viz::factories::codecs::bmp_t<channel_t>;

// encode color channels whose values fall outside the unit interval, and check that every one
// lands on the nearest end of the byte range, with a value that is not a number counted as zero;
// the tile is wide enough for the compiler to vectorize the loop over its columns
int
main(int argc, char * argv[])
{
    // a square tile whose lines need no padding
    const int height = 16;
    const int width = 16;
    auto shape = channel_t::shape_type(height, width);
    // make the color channels: too bright, too dark, and not a number
    auto red = channel_t::create("red", shape, 22.5);
    auto green = channel_t::create("green", shape, -3.0);
    auto blue = channel_t::create("blue", shape, std::numeric_limits<cell_t>::quiet_NaN());
    // and the resulting image
    auto image = image_t::create("img", shape);
    // make the encoder
    auto codec = codec_t::create("codec");
    // wire it
    codec->red(red);
    codec->green(green);
    codec->blue(blue);
    codec->image(image);
    // encode
    auto data = image->read();

    // the size of a header
    const int header = 54;
    // the bytes of a line
    const int line = width * 3;
    // the bitmap holds the header and every line
    assert(data.cells() == header + height * line);
    // go through the lines
    for (int row = 0; row < height; ++row) {
        // the start of the line
        auto start = data.data() + header + row * line;
        // go through its pixels
        for (int col = 0; col < width; ++col) {
            // the blue byte is not a number, so it is dark
            assert(start[3 * col + 0] == 0x00);
            // the green byte is below the interval, so it is dark
            assert(start[3 * col + 1] == 0x00);
            // and the red byte is above it, so it is as bright as a byte can be
            assert(start[3 * col + 2] == 0xff);
        }
    }

    // all done
    return 0;
}


// end of file
