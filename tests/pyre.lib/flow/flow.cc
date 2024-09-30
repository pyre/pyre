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
#include <pyre/flow.h>


// type aliases
using factory_t = pyre::flow::factory_t;
using product_t = pyre::flow::product_t;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow");
    // turn it on
    // channel.activate();

    // signal
    auto signal = product_t::create();
    // selector
    auto amplitude = factory_t::create();
    // the data tile
    auto tile = product_t::create();
    // encoder
    auto encoder = factory_t::create();
    // bitmap
    auto bmp = product_t::create();

    // set up the workflow
    amplitude->addInput("signal", signal);
    amplitude->addOutput("data", tile);
    encoder->addInput("data", tile);
    encoder->addOutput("bmp", bmp);

    // refresh the bitmap
    bmp->make();

    // tear down the workflow
    amplitude->removeInput("signal");
    amplitude->removeOutput("data");
    encoder->removeInput("data");
    encoder->removeOutput("bmp");

    // verify that amplitude has no bindings
    // get its inputs
    auto & amplitudeInputs = amplitude->inputs();
    // verify its an empty container
    assert(amplitudeInputs.size() == 0);
    // get its outputs
    auto & amplitudeOutputs = amplitude->outputs();
    // verify its an empty container
    assert(amplitudeOutputs.size() == 0);

    // verify that encoder has no bindings
    // get its inputs
    auto & encoderInputs = encoder->inputs();
    // verify its an empty container
    assert(encoderInputs.size() == 0);
    // get its outputs
    auto & encoderOutputs = encoder->outputs();
    // verify its an empty container
    assert(encoderOutputs.size() == 0);

    // all done
    return 0;
}


// end of file
