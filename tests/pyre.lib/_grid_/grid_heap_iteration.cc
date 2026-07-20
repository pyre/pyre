// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <iterator>
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


// verify that walking a grid visits its cells in packing order
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("grid_heap_iteration");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.grid");

    // a cursor over the cells of a grid is a genuine forward iterator, so that the standard
    // algorithms and the range based {for} accept it
    static_assert(std::forward_iterator<grid_t::iterator>);

    // pick a shape
    constexpr shape_t shape { 2, 3, 4 };
    // lay it out canonically over enough cells to hold it
    const canonical_t packing { shape };
    // put the cells on the heap
    const heap_t store { packing.cells() };
    // and make a grid
    const grid_t grid { packing, store };

    // stamp every cell with its own offset, reaching them by index
    for (auto it = grid.packing().begin(); it != grid.packing().end(); ++it) {
        // so that the sweep below has something recognizable to find
        grid[*it] = static_cast<grid_t::value_type>(packing.offset(*it));
    }

    // now walk the cells rather than the indices
    // the count of what we have seen so far doubles as the offset we expect next, because a
    // sweep in packing order visits consecutive cells of the block
    grid_t::difference_type seen = 0;
    // range based {for} is the point of the exercise
    for (auto cell : grid) {
        // show me
        channel << pyre::journal::at() << "  cell " << seen << " -> " << cell
                << pyre::journal::newline;
        // each cell carries the offset it was stamped with, so the sweep must arrive in order
        assert((cell == static_cast<grid_t::value_type>(seen)));
        // and on to the next
        ++seen;
    }
    // the sweep must have accounted for every cell
    assert((seen == packing.cells()));

    // writing through a cursor must reach the cell it is parked on
    auto cursor = grid.begin();
    // put something recognizable there
    *cursor = -3;
    // and find it through the index that names the same cell
    assert((grid[index_t { 0, 0, 0 }] == -3));

    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
