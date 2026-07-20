// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/_grid_.h>
// and the storage strategies
#include <pyre/memory.h>


// the parts of the grid under test
using canonical_t = pyre::grid::canonical_t<3>;
using heap_t = pyre::memory::heap_t<pyre::memory::float64_t>;
using grid_t = pyre::grid::grid_t<canonical_t, heap_t>;
// and the pieces used to address it
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;


// write a value into every cell of a grid and read them all back
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("grid_heap_access");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.grid");

    // pick a shape
    constexpr shape_t shape { 2, 3, 4 };
    // lay it out canonically
    const canonical_t packing { shape };
    // and put enough cells on the heap to hold it
    const heap_t store { packing.cells() };
    // which together make a grid
    const grid_t grid { packing, store };

    // fill every cell with a value that encodes where it lives, so that a cell read back from
    // the wrong place is visible rather than merely wrong
    for (auto it = grid.packing().begin(); it != grid.packing().end(); ++it) {
        // name the cell
        auto idx = *it;
        // and stamp it with its own offset
        grid[idx] = static_cast<grid_t::value_type>(packing.offset(idx));
    }

    // now go back over the grid
    for (auto it = grid.packing().begin(); it != grid.packing().end(); ++it) {
        // name the cell
        auto idx = *it;
        // work out where it should have landed
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
    assert((grid[index_t { 1, 2, 3 }] == grid[packing.offset(index_t { 1, 2, 3 })]));

    // writing through one path must be visible from the other
    grid[index_t { 0, 0, 0 }] = 42;
    // so read it back the long way round
    assert((grid.at(packing.offset(index_t { 0, 0, 0 })) == 42));

    // all done
    return 0;
}


// end of file
