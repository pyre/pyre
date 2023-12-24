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

// my slots
#include "../../products/memory/TileF4.h"
// my class declaration
#include "Gray.h"

// destructor
pyre::viz::factories::colormaps::Gray::~Gray() {}

// accessors
auto
pyre::viz::factories::colormaps::Gray::data() -> channel_ref_type
{
    // look up the product bound to my {data} slot and return it
    return std::dynamic_pointer_cast<channel_type>(input("data"));
}

auto
pyre::viz::factories::colormaps::Gray::red() -> channel_ref_type
{
    // look up the product bound to my {red} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("red"));
}

auto
pyre::viz::factories::colormaps::Gray::green() -> channel_ref_type
{
    // look up the product bound to my {green} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("green"));
}

auto
pyre::viz::factories::colormaps::Gray::blue() -> channel_ref_type
{
    // look up the product bound to my {blue} slot and return it
    return std::dynamic_pointer_cast<channel_type>(output("blue"));
}

// mutators
auto
pyre::viz::factories::colormaps::Gray::data(channel_ref_type data) -> factory_ref_type
{
    // connect my {data} slot
    addInput("data", std::static_pointer_cast<pyre::flow::product_t>(data));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Gray>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::Gray::red(channel_ref_type red) -> factory_ref_type
{
    // connect my {red} slot
    addOutput("red", std::static_pointer_cast<pyre::flow::product_t>(red));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Gray>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::Gray::green(channel_ref_type green) -> factory_ref_type
{
    // connect my {green} slot
    addOutput("green", std::static_pointer_cast<pyre::flow::product_t>(green));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Gray>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::Gray::blue(channel_ref_type blue) -> factory_ref_type
{
    // connect my {blue} slot
    addOutput("blue", std::static_pointer_cast<pyre::flow::product_t>(blue));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Gray>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::colormaps::Gray::make(
    const name_type & slot, base_type::product_ref_type product) -> base_type::factory_ref_type
{
    // chain up
    auto self = base_type::make(slot, product);

    // get my data
    auto i = data();
    // get my color channels
    auto r = red();
    auto g = green();
    auto b = blue();

    // the bound products must be shape compatible; the current implementation only requires
    // that products have the same number of cells
    auto pixels = i->shape().cells();
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
            << "gray factory at " << this << ":"
            << pyre::journal::newline
            // what
            << "shape mismatch in the input and output slots"
            << pyre::journal::newline
            // inputs
            << "inputs "
            << pyre::journal::newline
            // indent
            << pyre::journal::indent
            // image
            << "data: " << i->shape()
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

    // gray is boring: it copies its input to its three output slots
    // get the data buffers
    auto iData = i->read();
    auto rData = r->write();
    auto gData = g->write();
    auto bData = b->write();
    // copy
    for (auto pixel = 0; pixel < pixels; ++pixel) {
        // read
        auto value = iData[pixel];
        // write
        rData[pixel] = value;
        gData[pixel] = value;
        bData[pixel] = value;
    }

    // all done
    return self;
}

// end of file
