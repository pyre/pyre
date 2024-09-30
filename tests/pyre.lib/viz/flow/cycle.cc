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
using signal_cell_t = std::complex<float>;
using signal_storage_t = pyre::memory::heap_t<signal_cell_t>;
using signal_grid_t = pyre::grid::grid_t<packing_t, signal_storage_t>;
using signal_t = pyre::flow::products::tile_t<signal_grid_t>;
// the output
using cycle_cell_t = double;
using cycle_storage_t = pyre::memory::heap_t<cycle_cell_t>;
using cycle_grid_t = pyre::grid::grid_t<packing_t, cycle_storage_t>;
using cycle_t = pyre::flow::products::tile_t<cycle_grid_t>;
// the factory
using filter_t = pyre::viz::factories::filters::cycle_t<signal_t, cycle_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // pick a shape
    auto shape = cycle_t::shape_type(512, 512);
    // make a signal tile
    auto signal = signal_t::create("signal", shape, { 0.5, 0.5 });
    // make a cycle tile
    auto cycle = cycle_t::create("cycle", shape, 0);
    // make the filter
    auto filter = filter_t::create("cycle", { 0, 1 });
    // wire it
    filter->signal(signal);
    filter->cycle(cycle);

    // go through the tile contents
    for (auto v : cycle->read()) {
        // check
        assert((std::abs(v - 0.125) < 1e-5));
    }

    // pick another interval
    filter->interval({ 0, 100 });
    // go through the output contents
    for (auto v : cycle->read()) {
        // check that they reflect the new value
        assert((std::abs(v - 12.5) < 1e-3));
    }

    // all done
    return 0;
}

// end of file