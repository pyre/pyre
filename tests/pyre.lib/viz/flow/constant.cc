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
using cell_t = float;
using packing_t = pyre::grid::canonical_t<2>;
using storage_t = pyre::memory::heap_t<cell_t>;
using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
using tile_t = pyre::flow::products::tile_t<grid_t>;
using constant_t = pyre::viz::factories::filters::constant_t<tile_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // make a tile
    auto tile = tile_t::create("tile_f4_heap", { 512, 512 });
    // pick a value
    cell_t value = 1;
    // make the factory
    auto constant = constant_t::create("constant", value);
    // wire it
    constant->tile(tile);

    // go through the tile contents
    for (auto v : tile->read()) {
        // check
        assert((v == value));
    }

    // pick another value
    value = 2;
    // modify the factory
    constant->value(value);
    // go through the tile contents
    for (auto v : tile->read()) {
        // check that they reflect the new value
        assert((v == value));
    }

    // all done
    return 0;
}

// end of file