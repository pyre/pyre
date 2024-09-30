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
using parametric_cell_t = double;
using parametric_storage_t = pyre::memory::heap_t<parametric_cell_t>;
using parametric_grid_t = pyre::grid::grid_t<packing_t, parametric_storage_t>;
using parametric_t = pyre::flow::products::tile_t<parametric_grid_t>;
// the factory
using filter_t = pyre::viz::factories::filters::parametric_t<signal_t, parametric_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // pick a shape
    auto shape = parametric_t::shape_type(512, 512);
    // make a signal tile
    auto signal = signal_t::create("signal", shape, 0.5);
    // make a parametric tile
    auto parametric = parametric_t::create("parametric", shape, 0);
    // make the filter
    auto filter = filter_t::create("parametric", { 0, 1 });
    // wire it
    filter->signal(signal);
    filter->parametric(parametric);

    // go through the tile contents
    for (auto v : parametric->read()) {
        // check; we've picked a value that is representable exactly, so no need to be careful
        // with the equality check
        assert((v == 0.5));
    }

    // pick another interval
    filter->interval({ 0, 100 });
    // go through the output contents
    for (auto v : parametric->read()) {
        // check that they reflect the new value
        assert((v == 0.5 / 100));
    }

    // all done
    return 0;
}

// end of file