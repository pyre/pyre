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
// all tiles are 2d
using packing_t = pyre::grid::canonical_t<2>;
// the input signal
using signal_cell_t = float;
using signal_storage_t = pyre::memory::heap_t<signal_cell_t>;
using signal_grid_t = pyre::grid::grid_t<packing_t, signal_storage_t>;
using signal_t = pyre::flow::products::tile_t<signal_grid_t>;
// the output
using power_cell_t = double;
using power_storage_t = pyre::memory::heap_t<power_cell_t>;
using power_grid_t = pyre::grid::grid_t<packing_t, power_storage_t>;
using power_t = pyre::flow::products::tile_t<power_grid_t>;
// the factory
using filter_t = pyre::viz::factories::filters::power_t<signal_t, power_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // pick a signal value
    auto value = signal_cell_t(0.5);
    // peak the filter parameters
    auto scale = 2;
    auto mean = 2;
    auto exponent = .75;
    // pick a shape
    auto shape = power_t::shape_type(512, 512);
    // make a signal tile
    auto signal = signal_t::create("signal", shape, value);
    // make a power tile
    auto power = power_t::create("power", shape, 0);
    // make the filter
    auto filter = filter_t::create("power", mean, scale, exponent);
    // wire it
    filter->signal(signal);
    filter->power(power);

    // do the math
    auto expected = scale * std::pow(value / mean, exponent);
    // go through the tile contents
    for (auto v : power->read()) {
        // check
        assert((std::abs(v - expected) < 1e-5));
    }

    // all done
    return 0;
}

// end of file