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
using cell_t = float;
using packing_t = pyre::grid::canonical_t<2>;
using storage_t = pyre::memory::heap_t<cell_t>;
using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
using channel_t = pyre::flow::products::tile_t<grid_t>;
using image_t = pyre::viz::products::images::bmp_t;
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
    // show me
    channel
        // the value
        << "bmp: " << data.cells() << " bytes of data at " << data.where()
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);

    // open a file
    auto stream = std::ofstream("pyre_viz_flow_bmp.bmp", std::ios::out | std::ios::binary);
    // if successful
    if (stream.is_open()) {
        // write the bytes
        stream.write(reinterpret_cast<const char *>(data.data()), data.cells());
    }

    // all done
    return 0;
}

// end of file