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
#include "../../products/memory/TileF4.h"
// my class declaration
#include "HSB.h"

// destructor
pyre::viz::factories::colormaps::HSB::~HSB() {}

// accessors
auto
pyre::viz::factories::colormaps::HSB::hue() -> channel_ref_type
{
    // look up the product bound to my {hue} slot and return it
    return std::dynamic_pointer_cast<channel_type>(input("hue"));
}

auto
pyre::viz::factories::colormaps::HSB::saturation() -> channel_ref_type
{
    // look up the product bound to my {saturation} slot and return it
    return std::dynamic_pointer_cast<channel_type>(input("saturation"));
}

auto
pyre::viz::factories::colormaps::HSB::brightness() -> channel_ref_type
{
    // look up the product bound to my {brightness} slot and return it
    return std::dynamic_pointer_cast<channel_type>(input("brightness"));
}

auto
pyre::viz::factories::colormaps::HSB::red() -> channel_ref_type
{
    // look up the product bound to my {red} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("red"));
}

auto
pyre::viz::factories::colormaps::HSB::green() -> channel_ref_type
{
    // look up the product bound to my {green} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("green"));
}

auto
pyre::viz::factories::colormaps::HSB::blue() -> channel_ref_type
{
    // look up the product bound to my {blue} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("blue"));
}

// mutators
auto
pyre::viz::factories::colormaps::HSB::hue(channel_ref_type hue) -> factory_ref_type
{
    // connect my {hue} slot
    addInput("hue", std::static_pointer_cast<pyre::flow::product_t>(hue));
    // make a self reference
    auto self = std::dynamic_pointer_cast<HSB>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::HSB::saturation(channel_ref_type saturation) -> factory_ref_type
{
    // connect my {saturation} slot
    addInput("saturation", std::static_pointer_cast<pyre::flow::product_t>(saturation));
    // make a self reference
    auto self = std::dynamic_pointer_cast<HSB>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::HSB::brightness(channel_ref_type brightness) -> factory_ref_type
{
    // connect my {brightness} slot
    addInput("brightness", std::static_pointer_cast<pyre::flow::product_t>(brightness));
    // make a self reference
    auto self = std::dynamic_pointer_cast<HSB>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::HSB::red(channel_ref_type red) -> factory_ref_type
{
    // connect my {red} slot
    addOutput("red", std::static_pointer_cast<pyre::flow::product_t>(red));
    // make a self reference
    auto self = std::dynamic_pointer_cast<HSB>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::HSB::green(channel_ref_type green) -> factory_ref_type
{
    // connect my {green} slot
    addOutput("green", std::static_pointer_cast<pyre::flow::product_t>(green));
    // make a self reference
    auto self = std::dynamic_pointer_cast<HSB>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::HSB::blue(channel_ref_type blue) -> factory_ref_type
{
    // connect my {blue} slot
    addOutput("blue", std::static_pointer_cast<pyre::flow::product_t>(blue));
    // make a self reference
    auto self = std::dynamic_pointer_cast<HSB>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::HSB::make(
    const name_type & slot, base_type::product_ref_type product) -> base_type::factory_ref_type
{
    // chain up
    auto self = base_type::make(slot, product);

    // get my data
    auto h = hue();
    auto s = saturation();
    auto v = brightness();
    // get my color channels
    auto r = red();
    auto g = green();
    auto b = blue();

    // the bound products must be shape compatible; the current implementation only requires
    // that products have the same number of cells
    auto pixels = h->shape().cells();
    // verify consistency
    bool ok =
        // check s
        pixels == s->shape().cells() &&
        // check l
        pixels == v->shape().cells() &&
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
            << "hsb factory at " << this << ":"
            << pyre::journal::newline
            // what
            << "shape mismatch in the input and output slots"
            << pyre::journal::newline
            // inputs
            << "inputs "
            << pyre::journal::newline
            // indent
            << pyre::journal::indent
            // hue
            << "hue: " << h->shape()
            << pyre::journal::newline
            // saturation
            << "saturation: " << s->shape()
            << pyre::journal::newline
            // brightness
            << "brightness: " << v->shape()
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
    // inputs
    auto hData = h->read();
    auto sData = s->read();
    auto vData = v->read();
    // outputs
    auto rData = r->write();
    auto gData = g->write();
    auto bData = b->write();

    // color convert
    for (auto pixel = 0; pixel < pixels; ++pixel) {
        // read
        auto hValue = hData[pixel];
        auto sValue = sData[pixel];
        auto vValue = vData[pixel];
        // project to rgb
        auto [rValue, gValue, bValue] = pyre::viz::colorspaces::hsb(hValue, sValue, vValue);
        // and write
        rData[pixel] = rValue;
        gData[pixel] = gValue;
        bData[pixel] = bValue;
    }

    // mark all products as clean
    r->clean();
    g->clean();
    b->clean();

    // all done
    return self;
}

// end of file
