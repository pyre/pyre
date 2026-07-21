// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>
// and the storage strategies
#include <pyre/memory.h>


// the parts of the grid under test
using canonical_t = pyre::grid::canonical_t<3>;
using heap_t = pyre::memory::heap_t<pyre::memory::float64_t>;
using grid_t = pyre::grid::grid_t<canonical_t, heap_t>;
// and the pieces used to address it
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;


// verify that a sub-grid addresses the cells of the grid it came from
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("grid_heap_box");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.grid");

    // pick a shape
    constexpr shape_t shape { 2, 3, 4 };
    // lay it out canonically over enough cells to hold it
    const canonical_t packing { shape };
    // put the cells on the heap
    const heap_t store { packing.cells() };
    // and make a grid
    const grid_t grid { packing, store };

    // start from a known state: stamp every cell with its own offset
    for (auto it = grid.packing().begin(); it != grid.packing().end(); ++it) {
        // so that a cell reached by two different routes is recognizable
        grid[*it] = static_cast<grid_t::value_type>(packing.offset(*it));
    }

    // carve out a sub-grid in the far corner
    const auto tile = grid.box(index_t { 1, 1, 1 }, shape_t { 1, 2, 3 });
    // it reports the extent it was asked for
    assert((tile.packing().shape() == shape_t { 1, 2, 3 }));
    // and it is anchored where we said
    assert((tile.packing().origin() == index_t { 1, 1, 1 }));

    // every cell of the sub-grid must be a cell of the parent, not a copy
    for (auto it = tile.packing().begin(); it != tile.packing().end(); ++it) {
        // name the cell
        auto idx = *it;
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << tile[idx]
                << pyre::journal::newline;
        // reaching it through the sub-grid and through the parent must agree
        assert((tile[idx] == grid[idx]));
    }

    // writing through the sub-grid must be visible in the parent
    tile[index_t { 1, 1, 1 }] = -7;
    // so ask the parent
    assert((grid[index_t { 1, 1, 1 }] == -7));

    // and writing through the parent must be visible in the sub-grid
    grid[index_t { 1, 2, 3 }] = -9;
    // so ask the sub-grid
    assert((tile[index_t { 1, 2, 3 }] == -9));

    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
