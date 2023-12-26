// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>


// type aliases
using packing_t = pyre::grid::canonical_t<2>;
using storage_t = pyre::memory::heap_t<float>;
using product_t = pyre::viz::products::memory::tile_t<packing_t, storage_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.products.memory.tile");
    // turn it on
    // channel.activate();

    // make a tile
    auto tile = product_t::create("tile_f4_heap", { 512, 512 }, 0);

    // all done
    return 0;
}

// end of file