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
using affine_cell_t = double;
using affine_storage_t = pyre::memory::heap_t<affine_cell_t>;
using affine_grid_t = pyre::grid::grid_t<packing_t, affine_storage_t>;
using affine_t = pyre::flow::products::tile_t<affine_grid_t>;
// the factory
using filter_t = pyre::viz::factories::filters::affine_t<signal_t, affine_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // pick a shape
    auto shape = affine_t::shape_type(512, 512);
    // make a signal tile
    auto signal = signal_t::create("signal", shape, 0.5);
    // make a affine tile
    auto affine = affine_t::create("affine", shape, 0);
    // make the filter
    auto filter = filter_t::create("affine", { 0, 1 });
    // wire it
    filter->signal(signal);
    filter->affine(affine);

    // go through the tile contents
    for (auto v : affine->read()) {
        // check; we've picked a value that is representable exactly, so no need to be careful
        // with the equality check
        assert((v == 0.5));
    }

    // pick another interval
    filter->interval({ 0, 100 });
    // go through the output contents
    for (auto v : affine->read()) {
        // check that they reflect the new value
        assert((v == 50));
    }

    // all done
    return 0;
}

// end of file