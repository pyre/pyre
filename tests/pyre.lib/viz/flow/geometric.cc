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
// the output bins
using bin_cell_t = int;
using bin_storage_t = pyre::memory::heap_t<bin_cell_t>;
using bin_grid_t = pyre::grid::grid_t<packing_t, bin_storage_t>;
using bin_t = pyre::flow::products::tile_t<bin_grid_t>;
// the factory
using geometric_t = pyre::viz::factories::filters::geometric_t<signal_t, bin_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // pick a shape
    // auto shape = bin_t::shape_type(512, 512);
    auto shape = bin_t::shape_type(2, 2);
    // make a signal tile
    auto signal = signal_t::create("signal", shape, 0.5);
    // make a bin tile
    auto bin = bin_t::create("bin", shape, 0);
    // make the factory
    auto filter = geometric_t::create("geometric", 10);
    // wire it
    filter->signal(signal);
    filter->bin(bin);

    // go through the tile contents
    for (auto v : bin->read()) {
        // check
        assert((v == 9));
    }

    // all done
    return 0;
}

// end of file