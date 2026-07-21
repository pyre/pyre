// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <cstdio>
// get the grid
#include <pyre/grid.h>
// and the storage strategies
#include <pyre/memory.h>


// the parts of the grid under test: a canonical layout over a file backed store
using canonical_t = pyre::grid::canonical_t<3>;
using map_t = pyre::memory::map_t<pyre::memory::float64_t>;
using grid_t = pyre::grid::grid_t<canonical_t, map_t>;
// and the pieces used to address it
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;


// verify that a grid reads and writes cells that live in a memory mapped file
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("grid_map_access");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.grid");

    // the file that backs this grid; a fresh name so a stale run cannot mislead us
    const char * uri = "grid_map_access.data";

    // pick a shape
    constexpr shape_t shape { 2, 3, 4 };
    // lay it out canonically
    const canonical_t packing { shape };
    // create a fresh file sized to hold exactly its cells, and back the grid with it
    const map_t store = map_t::create(uri, packing.cells());
    // and make a grid over the two
    const grid_t grid { packing, store };

    // stamp every cell with its own offset, which the mapping writes through to the file
    for (auto it = grid.packing().begin(); it != grid.packing().end(); ++it) {
        // each cell remembers where it lives
        grid[*it] = static_cast<grid_t::value_type>(packing.offset(*it));
    }

    // read them all back
    for (auto it = grid.packing().begin(); it != grid.packing().end(); ++it) {
        // name the cell
        auto idx = *it;
        // what it should hold
        auto expected = static_cast<grid_t::value_type>(packing.offset(idx));
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << grid[idx]
                << pyre::journal::newline;
        // the value must have survived the round trip through the file
        assert((grid[idx] == expected));
    }
    // flush the trace
    channel << pyre::journal::endl;

    // the origin lands at the beginning of the file
    assert((grid[index_t { 0, 0, 0 }] == 0));

    // done with the backing file
    std::remove(uri);

    // all done
    return 0;
}


// end of file
