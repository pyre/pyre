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
using logsaw_cell_t = double;
using logsaw_storage_t = pyre::memory::heap_t<logsaw_cell_t>;
using logsaw_grid_t = pyre::grid::grid_t<packing_t, logsaw_storage_t>;
using logsaw_t = pyre::flow::products::tile_t<logsaw_grid_t>;
// the factory
using filter_t = pyre::viz::factories::filters::logsaw_t<signal_t, logsaw_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // pick a value
    auto value = signal_cell_t(0.5, 0.5);
    // pick a shape
    auto shape = logsaw_t::shape_type(512, 512);
    // make a signal tile
    auto signal = signal_t::create("signal", shape, value);
    // make a logsaw tile
    auto logsaw = logsaw_t::create("logsaw", shape, 0);
    // make the filter
    auto filter = filter_t::create("logsaw");
    // wire it
    filter->signal(signal);
    filter->logsaw(logsaw);

    // do the math
    auto log = std::log2(std::abs(value));
    auto expected = std::abs(log - std::trunc(log));
    // go through the tile contents
    for (auto v : logsaw->read()) {
        // check
        assert((std::abs(v - expected) < 1e-5));
    }

    // all done
    return 0;
}

// end of file