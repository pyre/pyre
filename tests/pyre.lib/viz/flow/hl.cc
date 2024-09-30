// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>

// type aliases
// all tiles are two dimensional
using packing_t = pyre::grid::canonical_t<2>;
// the color channels
using pixel_t = float;
using color_storage_t = pyre::memory::heap_t<pixel_t>;
using color_grid_t = pyre::grid::grid_t<packing_t, color_storage_t>;
using channel_t = pyre::flow::products::tile_t<color_grid_t>;
// the image
using image_t = pyre::viz::products::images::bmp_t;
// the colormap
using color_t = pyre::viz::factories::colormaps::hl_t<channel_t>;
// the codec
using codec_t = pyre::viz::factories::codecs::bmp_t<channel_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow");
    // turn it on
    // channel.activate();

    // pick a shape
    auto shape = channel_t::shape_type(512, 512);
    // make the input data
    auto hue = channel_t::create("hue", shape, 0 * 2 * M_PI / 3);
    auto luminosity = channel_t::create("luminosity", shape, 0.5);
    // make the color channels
    auto red = channel_t::create("red", shape, 0.25);
    auto green = channel_t::create("green", shape, 0.50);
    auto blue = channel_t::create("blue", shape, 1.00);
    // and the resulting image
    auto image = image_t::create("img", shape);

    // make the colorspace
    auto hl = color_t::create("hl");
    // wire it
    hl->hue(hue);
    hl->luminosity(luminosity);
    hl->red(red);
    hl->green(green);
    hl->blue(blue);

    // make the encoder
    auto codec = codec_t::create("codec");
    // wire it
    codec->red(red);
    codec->green(green);
    codec->blue(blue);
    codec->image(image);

    // encode
    auto img = image->read();
    // show me
    channel
        // the value
        << "bmp: " << img.cells() << " bytes of data at " << img.where()
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);

    // open a file
    auto stream = std::ofstream("pyre_viz_flow_hl.bmp", std::ios::out | std::ios::binary);
    // if successful
    if (stream.is_open()) {
        // write the bytes
        stream.write(reinterpret_cast<const char *>(img.data()), img.cells());
    }

    // all done
    return 0;
}

// end of file