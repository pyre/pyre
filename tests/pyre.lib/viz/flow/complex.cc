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
using data_t = std::complex<double>;
// products
using signal_t = pyre::viz::products::memory::tile_c8_t;
using channel_t = pyre::viz::products::memory::tile_f4_t;
using image_t = pyre::viz::products::images::bmp_t;
// factories
using color_t = pyre::viz::factories::colormaps::complex_t;
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
    auto shape = channel_t::shape_type(1001, 1001);
    // make the input data
    auto signal = signal_t::create("signal", shape, 0.0);
    // its data grid
    auto & grid = signal->write();
    // we are discretizing the unit square centered at the origin
    // for a given number of bins; the spacing is
    const double delta = 1.0 / (shape[0] - 1);
    // loop over the shape
    for (const auto & idx : grid.layout()) {
        // unpack
        auto [i, j] = idx;
        // convert the indices into a complex number in our space
        data_t z { -0.5 + j * delta, 0.5 - i * delta };
        // and place the value in the input grid
        grid[idx] = z;
    }

    // make the color channels
    auto red = channel_t::create("red", shape, 0.0);
    auto green = channel_t::create("green", shape, 0.0);
    auto blue = channel_t::create("blue", shape, 0.0);
    // and the resulting image
    auto image = image_t::create("image", shape);

    // make the colorspace
    auto color = color_t::create("complex", 360, 1.0, .25, 1.0);
    // wire it
    color->signal(signal);
    color->red(red);
    color->green(green);
    color->blue(blue);

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
    auto stream = std::ofstream("complex.bmp", std::ios::out | std::ios::binary);
    // if successful
    if (stream.is_open()) {
        // write the bytes
        stream.write(reinterpret_cast<const char *>(img.data()), img.cells());
    }

    // all done
    return 0;
}

// end of file