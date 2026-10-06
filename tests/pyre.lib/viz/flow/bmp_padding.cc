// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
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

// encode a tile that is taller than it is wide, and whose lines need padding, and check the size
// of the bitmap, its pixels, and the padding at the end of every line
int
main(int argc, char * argv[])
{
    // a tile with more lines than columns; five pixels make fifteen bytes, so every line needs
    // one byte of padding to land on a multiple of four
    const int height = 7;
    const int width = 5;
    auto shape = channel_t::shape_type(height, width);
    // make the color channels
    auto red = channel_t::create("red", shape, 0.25);
    auto green = channel_t::create("green", shape, 0.50);
    auto blue = channel_t::create("blue", shape, 1.00);
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
    // the bytes of a line, with its padding
    const int line = width * 3 + 1;
    // the bitmap holds the header and every line, padding included
    assert(data.cells() == header + height * line);
    // the bytes of the pixels, in the order the format wants them
    const unsigned char b = 0xff * 1.00;
    const unsigned char g = 0xff * 0.50;
    const unsigned char r = 0xff * 0.25;
    // go through the lines
    for (int row = 0; row < height; ++row) {
        // the start of the line
        auto start = data.data() + header + row * line;
        // go through its pixels
        for (int col = 0; col < width; ++col) {
            // check the blue byte
            assert(start[3 * col + 0] == b);
            // the green byte
            assert(start[3 * col + 1] == g);
            // and the red byte
            assert(start[3 * col + 2] == r);
        }
        // and the line ends with its padding
        assert(start[3 * width] == 0);
    }

    // all done
    return 0;
}


// end of file
