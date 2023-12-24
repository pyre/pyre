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
#include "Amplitude.h"

// destructor
pyre::viz::factories::selectors::Amplitude::~Amplitude() {}

// accessors
auto
pyre::viz::factories::selectors::Amplitude::signal() -> signal_ref_type
{
    // look up the product bound to my {hue} slot and return it
    return std::dynamic_pointer_cast<signal_type>(input("signal"));
}

auto
pyre::viz::factories::selectors::Amplitude::amplitude() -> amplitude_ref_type
{
    // look up the product bound to my {red} slot and return it
    return std::dynamic_pointer_cast<amplitude_type>(output("amplitude"));
}

// mutators
auto
pyre::viz::factories::selectors::Amplitude::signal(signal_ref_type signal) -> factory_ref_type
{
    // connect my {hue} slot
    addInput("signal", std::static_pointer_cast<pyre::flow::product_t>(signal));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Amplitude>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::selectors::Amplitude::amplitude(amplitude_ref_type amplitude)
    -> factory_ref_type
{
    // connect my {red} slot
    addOutput("amplitude", std::static_pointer_cast<pyre::flow::product_t>(amplitude));
    // make a self reference
    auto self = std::dynamic_pointer_cast<Amplitude>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::selectors::Amplitude::make(
    const name_type & slot, base_type::product_ref_type product) -> base_type::factory_ref_type
{
    // chain up
    auto self = base_type::make(slot, product);

    // get my input
    auto s = signal();
    // get my output
    auto a = amplitude();

    // the bound products must be shape compatible; the current implementation only requires
    // that products have the same number of cells
    auto pixels = s->shape().cells();
    // verify consistency
    bool ok = pixels == a->shape().cells();
    // if something is off
    if (!ok) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.viz.factories.selectors.amplitude");
        // complain
        channel
            // who
            << "amplitude factory '" << name() << "' at " << this << ":"
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
            // amplitude
            << "amplitude: " << a->shape()
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
    auto sData = s->read();
    // outputs
    auto aData = a->write();

    // go through the cells
    for (auto pixel = 0; pixel < pixels; ++pixel) {
        // read
        auto sValue = sData[pixel];
        // compute the amplitude and write
        aData[pixel] = std::abs(sValue);
    }

    // all done
    return self;
}

// end of file
