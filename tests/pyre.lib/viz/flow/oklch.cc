// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
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
using color_t = pyre::viz::factories::colormaps::oklch_t<channel_t>;
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
    // pick a color: a mid green, in perceptual coordinates, with its hue in degrees
    const float l = 0.7f;
    const float c = 0.15f;
    const float h = 140.0f;
    // make the input data
    auto lightness = channel_t::create("lightness", shape, l);
    auto chroma = channel_t::create("chroma", shape, c);
    auto hue = channel_t::create("hue", shape, h);
    // make the color channels
    auto red = channel_t::create("red", shape, 0.0);
    auto green = channel_t::create("green", shape, 0.0);
    auto blue = channel_t::create("blue", shape, 0.0);
    // and the resulting image
    auto image = image_t::create("img", shape);

    // make the colorspace
    auto oklch = color_t::create("oklch");
    // wire it
    oklch->lightness(lightness);
    oklch->chroma(chroma);
    oklch->hue(hue);
    oklch->red(red);
    oklch->green(green);
    oklch->blue(blue);

    // make the encoder
    auto codec = codec_t::create("bmp");
    // wire it
    codec->red(red);
    codec->green(green);
    codec->blue(blue);
    codec->image(image);

    // encode, which pulls the color channels through the colormap
    auto img = image->read();
    // show me
    channel
        // where
        << pyre::journal::at()
        // the value
        << "bmp: " << img.cells() << " bytes of data at " << img.where()
        << pyre::journal::newline
        // flush
        << pyre::journal::endl;

    // the color the kernel makes of these inputs, the same one the {oklch} iterator uses
    auto [r, g, b] = pyre::chroma::rgb::oklch(l, c, h);
    // the kernel is inlined at two different places, and a compiler that contracts multiplications
    // and additions differently at each may disagree in the last bits, so compare within a margin
    const double tolerance = 1.0e-5;
    // that says whether a channel carries the expected value
    auto close = [tolerance](double value, double expected) -> bool {
        // within the margin
        return std::abs(value - expected) <= tolerance;
    };
    // get the color channels
    auto & rData = red->read();
    auto & gData = green->read();
    auto & bData = blue->read();
    // every pixel of every channel must carry it
    for (auto pixel = 0; pixel < shape.cells(); ++pixel) {
        // check the red channel
        assert(close(rData[pixel], r));
        // the green channel
        assert(close(gData[pixel], g));
        // and the blue channel
        assert(close(bData[pixel], b));
    }

    // open a file
    auto stream = std::ofstream("pyre_viz_flow_oklch.bmp", std::ios::out | std::ios::binary);
    // if successful
    if (stream.is_open()) {
        // write the bytes
        stream.write(reinterpret_cast<const char *>(img.data()), img.cells());
    }

    // all done
    return 0;
}


// end of file
