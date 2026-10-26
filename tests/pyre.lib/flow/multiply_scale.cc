// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/journal.h>
#include <pyre/flow.h>


// type aliases
// pick a cell type
using cell_t = double;
// a packing
using packing_t = pyre::grid::canonical_t<2>;
// and a storage strategy
using storage_t = pyre::memory::heap_t<cell_t>;
// use them to make a grid
using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
// the tiles
using tile_t = pyre::flow::products::tile_t<grid_t>;
// and the scalars
using scalar_t = pyre::flow::products::var_t<cell_t>;
// the operator that scales a tile by a scalar on its right
using right_t = pyre::flow::factories::operators::multiply_t<tile_t, scalar_t>;
// and the one with the scalar on the left
using left_t = pyre::flow::factories::operators::multiply_t<scalar_t, tile_t>;

// driver
int
main(int argc, char * argv[])
{
    // pick a shape
    auto shape = tile_t::shape_type(8, 8);
    // make the tile
    auto tile = tile_t::create("tile", shape, 2);
    // and the scalar
    auto scalar = scalar_t::create("scalar", 3);
    // make the results
    auto right = tile_t::create("right", shape, 0);
    auto left = tile_t::create("left", shape, 0);

    // make the operator with the scalar on the right
    auto scaleRight = right_t::create("right");
    // wire it
    scaleRight->op1(tile);
    scaleRight->op2(scalar);
    scaleRight->result(right);
    // make the operator with the scalar on the left
    auto scaleLeft = left_t::create("left");
    // wire it
    scaleLeft->op1(scalar);
    scaleLeft->op2(tile);
    scaleLeft->result(left);

    // go through the cells of both results
    for (auto value : right->read()) {
        // and check them
        assert((value == 6));
    }
    for (auto value : left->read()) {
        // and check them
        assert((value == 6));
    }

    // change the scalar
    scalar->value(4);
    // and check that both results follow
    for (auto value : right->read()) {
        // one cell at a time
        assert((value == 8));
    }
    for (auto value : left->read()) {
        // one cell at a time
        assert((value == 8));
    }

    // all done
    return 0;
}


// end of file
