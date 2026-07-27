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
using chunked_t = pyre::grid::chunked_t<2>;
using heap_t = pyre::memory::heap_t<pyre::memory::float64_t>;
using grid_t = pyre::grid::grid_t<chunked_t, heap_t>;
// and the pieces used to address it
using shape_t = chunked_t::shape_type;
using index_t = chunked_t::index_type;


// compose a chunked packing with heap storage, write to every cell, and read them all back
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("grid_heap_chunked");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.chunked");

    // pick a box that is not a whole number of tiles, so the storage carries padding
    constexpr shape_t shape { 5, 7 };
    // and a tile extent
    constexpr shape_t tile { 2, 3 };
    // dice the box
    const chunked_t packing { shape, tile };
    // put enough cells on the heap to hold every tile at full size
    const heap_t store { packing.cells() };
    // which together make a grid
    const grid_t grid { packing, store };

    // fill every cell with a value that encodes where it lives, so that a cell read back from
    // the wrong place is visible rather than merely wrong
    for (auto idx : grid.packing()) {
        // stamp the cell with its own offset
        grid[idx] = static_cast<grid_t::value_type>(packing.offset(idx));
    }

    // now go back over the box
    for (auto idx : grid.packing()) {
        // work out what the cell should hold
        auto expected = static_cast<grid_t::value_type>(packing.offset(idx));
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << grid[idx]
                << pyre::journal::newline;
        // the unguarded path must find what we put there
        assert((grid[idx] == expected));
        // and so must the guarded one
        assert((grid.at(idx) == expected));
    }
    // flush the trace
    channel << pyre::journal::endl;

    // reaching by offset must agree with reaching by index
    assert((grid[index_t { 3, 5 }] == grid[packing.offset(index_t { 3, 5 })]));

    // writing through one path must be visible from the other
    grid[index_t { 4, 6 }] = 42;
    // so read it back the long way round
    assert((grid.at(packing.offset(index_t { 4, 6 })) == 42));

    // all done
    return 0;
}


// end of file
