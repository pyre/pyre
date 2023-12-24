// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// externals
#include "../external.h"
// forward declarations
#include "../forward.h"
// type aliases
#include "../api.h"

// my color projections
#include "../../colorspaces/hsb.h"
// my slots
#include "../../products/memory/TileC8.h"
#include "../../products/memory/TileF4.h"
// my class declaration
#include "Complex.h"

// destructor
pyre::viz::factories::colormaps::Complex::~Complex() {}

// accessors
auto
pyre::viz::factories::colormaps::Complex::signal() -> signal_ref_type
{
    // look up the product bound to my {signal} slot and return it
    return std::dynamic_pointer_cast<signal_type>(input("signal"));
}

auto
pyre::viz::factories::colormaps::Complex::red() -> channel_ref_type
{
    // look up the product bound to my {red} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("red"));
}

auto
pyre::viz::factories::colormaps::Complex::green() -> channel_ref_type
{
    // look up the product bound to my {green} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("green"));
}

auto
pyre::viz::factories::colormaps::Complex::blue() -> channel_ref_type
{
    // look up the product bound to my {blue} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("blue"));
}

// mutators
auto
pyre::viz::factories::colormaps::Complex::signal(signal_ref_type signal) -> factory_ref_type
{
    // connect my {signal} slot
    addInput("signal", std::static_pointer_cast<pyre::flow::product_t>(signal));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Complex>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::Complex::red(channel_ref_type red) -> factory_ref_type
{
    // connect my {red} slot
    addOutput("red", std::static_pointer_cast<pyre::flow::product_t>(red));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Complex>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::Complex::green(channel_ref_type green) -> factory_ref_type
{
    // connect my {green} slot
    addOutput("green", std::static_pointer_cast<pyre::flow::product_t>(green));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Complex>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::Complex::blue(channel_ref_type blue) -> factory_ref_type
{
    // connect my {blue} slot
    addOutput("blue", std::static_pointer_cast<pyre::flow::product_t>(blue));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Complex>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::Complex::make(
    const name_type & slot, base_type::product_ref_type product) -> base_type::factory_ref_type
{
    // chain up
    auto self = base_type::make(slot, product);

    // get my data
    auto s = signal();
    // get my color channels
    auto r = red();
    auto g = green();
    auto b = blue();

    // the bound products must be shape compatible; the current implementation only requires
    // that products have the same number of cells
    auto pixels = s->shape().cells();
    // verify consistency
    bool ok =
        // check r
        pixels == r->shape().cells() &&
        // check g
        pixels == g->shape().cells() &&
        // check b
        pixels == b->shape().cells();
    // if something is off
    if (!ok) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.viz.factories.bmp");
        // complain
        channel
            // who
            << "complex factory at " << this << ":"
            << pyre::journal::newline
            // what
            << "shape mismatch in the input and output slots"
            << pyre::journal::newline
            // inputs
            << "inputs "
            << pyre::journal::newline
            // indent
            << pyre::journal::indent
            // signal
            << "signal: " << s->shape()
            << pyre::journal::newline
            // outdent
            << pyre::journal::outdent
            // outputs
            << "outputs: "
            << pyre::journal::newline
            // indent
            << pyre::journal::indent
            // details
            // red
            << "red: " << r->shape()
            << pyre::journal::newline
            // green
            << "green: " << g->shape()
            << pyre::journal::newline
            // blue
            << "blue: " << b->shape()
            << pyre::journal::newline
            // outdent
            << pyre::journal::outdent
            // flush
            << pyre::journal::endl(__HERE__);
        // and bail, just in case errors aren't fatal
        return self;
    }

    // get the data buffers
    auto sData = s->read();
    auto rData = r->write();
    auto gData = g->write();
    auto bData = b->write();

    // color convert
    for (auto pixel = 0; pixel < pixels; ++pixel) {
        // the pixel color
        rgb_type color;
        // read
        auto value = sData[pixel];

        // compute the amplitude
        auto amplitude = std::abs(value);
        // if the value underflows
        if (amplitude < _minAmplitude) {
            // use whatever color the user has specified
            color = _underflow;
        } else if (amplitude > _maxAmplitude) {
            // use whatever color the user has specified
            color = _overflow;
        } else {
            // get the phase from the data source
            auto phase = std::arg(value);
            // bin the phase
            int hueBin = phase / _scaleHue;
            // compute the hue
            auto hue = hueBin * _scaleHue;
            // bin the amplitude
            int brightnessBin = (amplitude - _minAmplitude) / _scaleAmplitude;
            // compute the brightness
            auto brightness = _minBrightness + brightnessBin * _scaleBrightness;
            // convert the {hsl} values to {rgb} and return the triplet
            color = pyre::viz::colorspaces::hsb(hue, _saturation, brightness);
        }
        // unpack
        auto [rValue, gValue, bValue] = color;
        // and write
        rData[pixel] = rValue;
        gData[pixel] = gValue;
        bData[pixel] = bValue;
    }

    // all done
    return self;
}

// end of file
