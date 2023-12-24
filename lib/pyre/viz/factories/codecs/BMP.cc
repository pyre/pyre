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
#include "../../products/images/BMP.h"
#include "../../products/memory/TileF4.h"
// my class declaration
#include "BMP.h"

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
pyre::viz::factories::codecs::BMP::make(const name_type & slot, base_type::product_ref_type product)
    -> base_type::factory_ref_type
{
    // chain up
    auto self = base_type::make(slot, product);

    // get my color channels
    auto r = red();
    auto g = green();
    auto b = blue();
    // get my image
    auto bmp = image();

    // verify consistency
    bool ok = r->shape() == g->shape() && g->shape() == b->shape() && b->shape() == bmp->shape();
    // if something is off
    if (!ok) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.viz.factories.codecs.bmp");
        // complain
        channel
            // who
            << "bmp factory at " << this << ":"
            << pyre::journal::newline
            // what
            << "shape mismatch in the input and output slots"
            << pyre::journal::newline
            // when
            << "while making the image at " << bmp.get()
            << pyre::journal::newline
            // inputs
            << "inputs: "
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
            // outputs
            << "outputs "
            << pyre::journal::newline
            // indent
            << pyre::journal::indent
            // image
            << "image: " << bmp->shape()
            << pyre::journal::newline
            // outdent
            << pyre::journal::outdent
            // flush
            << pyre::journal::endl(__HERE__);
        // and bail, just in case errors aren't fatal
        return self;
    }

    // unpack the shape
    auto [height, width] = r->shape();
    // make iterators to the input channels
    auto redData = r->read().begin();
    auto greenData = g->read().begin();
    auto blueData = b->read().begin();
    // make an iterator to the image payload
    auto imageData = bmp->write().begin();

    // encode: go through the rows
    for (auto row = 0; row < height; ++row) {
        // go through the columns
        for (auto col = 0; col < width; ++col) {
            // get the pixel values
            pixel_type redPixel = static_cast<pixel_type>(0xff * (*redData++)) & 0xff;
            pixel_type greenPixel = static_cast<pixel_type>(0xff * (*greenData++)) & 0xff;
            pixel_type bluePixel = static_cast<pixel_type>(0xff * (*blueData++)) & 0xff;
            // encode; note that the order is {blue, green, red}
            *imageData++ = bluePixel;
            *imageData++ = greenPixel;
            *imageData++ = redPixel;
        }
        // done with this line
        for (auto pad = 0; pad < bmp->padding(); ++pad) {
            // add the pad bytes
            *imageData++ = 0;
        }
    }

    // all done
    return self;
}
// end of file
