// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>


// type aliases
using channel_t = pyre::viz::products::memory::tile_f4_t;
using image_t = pyre::viz::products::images::bmp_t;
using color_t = pyre::viz::factories::colorspaces::hsl_t;
using codec_t = pyre::viz::factories::codecs::bmp_t;

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
    auto hue = channel_t::create(shape, 2 * 2 * M_PI / 3);
    auto saturation = channel_t::create(shape, 1.0);
    auto luminosity = channel_t::create(shape, 0.5);
    // make the color channels
    auto red = channel_t::create(shape, 0.25);
    auto green = channel_t::create(shape, 0.50);
    auto blue = channel_t::create(shape, 1.00);
    // and the resulting image
    auto image = image_t::create(shape);

    // make the colorspace
    auto hsl = color_t::create();
    // wire it
    hsl->hue(hue);
    hsl->saturation(saturation);
    hsl->luminosity(luminosity);
    hsl->red(red);
    hsl->green(green);
    hsl->blue(blue);

    // make the encoder
    auto codec = codec_t::create();
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
    auto stream = std::ofstream("hsl.bmp", std::ios::out | std::ios::binary);
    // if successful
    if (stream.is_open()) {
        // write the bytes
        stream.write(reinterpret_cast<const char *>(img.data()), img.cells());
    }

    // all done
    return 0;
}

// end of file