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
// signal
using data_t = std::complex<double>;
using signal_storage_t = pyre::memory::heap_t<data_t>;
using signal_grid_t = pyre::grid::grid_t<packing_t, signal_storage_t>;
using signal_t = pyre::flow::products::tile_t<signal_grid_t>;
// color
using pixel_t = float;
using channel_storage_t = pyre::memory::heap_t<pixel_t>;
using channel_grid_t = pyre::grid::grid_t<packing_t, channel_storage_t>;
using channel_t = pyre::flow::products::tile_t<channel_grid_t>;
// image
using image_t = pyre::viz::products::images::bmp_t;
// selector
using imaginary_t = pyre::viz::factories::selectors::imaginary_t<signal_t, channel_t>;
// color map
using colormap_t = pyre::viz::factories::colormaps::gray_t<channel_t>;
// encoder
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

    // the imaginary
    auto imaginary = channel_t::create("imaginary", shape, 0.0);
    // make only one color channel
    auto gray = channel_t::create("gray", shape, 0.0);
    // and the resulting image
    auto image = image_t::create("image", shape);

    // make the selector
    auto selector = imaginary_t::create("imaginary");
    // wire it
    selector->signal(signal);
    selector->imaginary(imaginary);

    // make the colormap
    auto color = colormap_t::create("gray");
    // wire it
    color->data(imaginary);
    color->red(gray);
    color->green(gray);
    color->blue(gray);

    // make the encoder
    auto codec = codec_t::create("codec");
    // wire it
    codec->red(gray);
    codec->green(gray);
    codec->blue(gray);
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
    auto stream = std::ofstream("pyre_viz_flow_imaginary.bmp", std::ios::out | std::ios::binary);
    // if successful
    if (stream.is_open()) {
        // write the bytes
        stream.write(reinterpret_cast<const char *>(img.data()), img.cells());
    }

    // all done
    return 0;
}

// end of file