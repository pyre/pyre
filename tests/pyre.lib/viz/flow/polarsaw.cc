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
using polarsaw_cell_t = double;
using polarsaw_storage_t = pyre::memory::heap_t<polarsaw_cell_t>;
using polarsaw_grid_t = pyre::grid::grid_t<packing_t, polarsaw_storage_t>;
using polarsaw_t = pyre::flow::products::tile_t<polarsaw_grid_t>;
// the factory
using filter_t = pyre::viz::factories::filters::polarsaw_t<signal_t, polarsaw_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // pick a value
    auto value = signal_cell_t(M_PI);
    // pick a shape
    auto shape = polarsaw_t::shape_type(512, 512);
    // make a signal tile
    auto signal = signal_t::create("signal", shape, value);
    // make a polarsaw tile
    auto polarsaw = polarsaw_t::create("polarsaw", shape, 0);
    // make the filter
    auto filter = filter_t::create("polarsaw");
    // wire it
    filter->signal(signal);
    filter->polarsaw(polarsaw);

    // do the math
    auto saw = value * 6 / M_PI;
    auto expected = std::abs(saw - std::trunc(saw));
    // go through the tile contents
    for (auto v : polarsaw->read()) {
        // check
        assert((std::abs(v - expected) < 1e-5));
    }

    // all done
    return 0;
}

// end of file