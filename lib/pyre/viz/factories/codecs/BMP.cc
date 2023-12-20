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

// my class declaration
#include "BMP.h"
// my slots
#include "../../products/images/BMP.h"
#include "../../products/memory/TileF4.h"

// destructor
pyre::viz::factories::codecs::BMP::~BMP() {}

// accessors
auto
pyre::viz::factories::codecs::BMP::red() -> channel_ref_type
{
    // look up the product bound to my {red} slot and return it
    return std::dynamic_pointer_cast<channel_type>(input("red"));
}

auto
pyre::viz::factories::codecs::BMP::green() -> channel_ref_type
{
    // look up the product bound to my {green} slot and return it
    return std::dynamic_pointer_cast<channel_type>(input("green"));
}

auto
pyre::viz::factories::codecs::BMP::blue() -> channel_ref_type
{
    // look up the product bound to my {blue} slot and return it
    return std::dynamic_pointer_cast<channel_type>(input("blue"));
}

auto
pyre::viz::factories::codecs::BMP::image() -> image_ref_type
{
    // look up the product bound to my {image} slot and return it
    return std::dynamic_pointer_cast<image_type>(output("image"));
}

// mutators
auto
pyre::viz::factories::codecs::BMP::red(channel_ref_type red) -> factory_ref_type
{
    // connect my {red} slot
    addInput("red", std::static_pointer_cast<pyre::flow::product_t>(red));
    // make a self reference
    auto self = std::dynamic_pointer_cast<BMP>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::codecs::BMP::green(channel_ref_type green) -> factory_ref_type
{
    // connect my {green} slot
    addInput("green", std::static_pointer_cast<pyre::flow::product_t>(green));
    // make a self reference
    auto self = std::dynamic_pointer_cast<BMP>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::codecs::BMP::blue(channel_ref_type blue) -> factory_ref_type
{
    // connect my {blue} slot
    addInput("blue", std::static_pointer_cast<pyre::flow::product_t>(blue));
    // make a self reference
    auto self = std::dynamic_pointer_cast<BMP>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::codecs::BMP::image(image_ref_type image) -> factory_ref_type
{
    // connect my {image} slot
    addOutput("image", std::static_pointer_cast<pyre::flow::product_t>(image));
    // make a self reference
    auto self = std::dynamic_pointer_cast<BMP>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::codecs::BMP::make(name_type slot, base_type::product_ref_type product)
    -> base_type::factory_ref_type
{
    // chain up
    auto self = base_type::make(slot, product);

    // make a channel
    auto channel = pyre::journal::firewall_t("pyre.viz.factories.codecs.bmp");
    // complain
    channel
        // what
        << "NYI: 'make' is not implemented"
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return self;
}
// end of file
