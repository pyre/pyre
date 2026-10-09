// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that canonical packings and grids spell their types the same way on every compiler


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/grid.h>


// type aliases
// a two dimensional canonical packing
using packing_t = pyre::grid::canonical_t<2>;
// a grid of doubles on the heap
using grid_t = pyre::grid::grid_t<packing_t, pyre::memory::heap_t<double>>;


// driver
int
main(int argc, char * argv[])
{
    // the packing spells its declaration through the type alias, with its rank
    assert(packing_t::declSelf() == "pyre::grid::canonical_t<2>");
    // and its readable name with its rank
    assert(packing_t::className() == "Canonical2D");
    // the grid spells its declaration with the ones of its two strategies
    assert(
        grid_t::declSelf()
        == "pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<double>>");
    // and its readable name likewise
    assert(grid_t::className() == "GridCanonical2DHeapDouble");
    // all done
    return 0;
}


// end of file
