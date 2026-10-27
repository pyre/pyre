// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a scalar made by a factory scales a tile, and that the product follows when the
// factory changes its mind


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
// the factory that makes the scalar
using constant_t = pyre::flow::factories::filters::constant_t<scalar_t>;
// and the operator that scales a tile by it
using multiply_t = pyre::flow::factories::operators::multiply_t<scalar_t, tile_t>;

// driver
int
main(int argc, char * argv[])
{
    // pick a shape
    auto shape = tile_t::shape_type(8, 8);
    // make the tile
    auto tile = tile_t::create("tile", shape, 2);
    // the scalar
    auto scalar = scalar_t::create("scalar");
    // and the result
    auto result = tile_t::create("result", shape, 0);

    // make the factory of the scalar
    auto constant = constant_t::create("constant", 3);
    // wire it
    constant->result(scalar);
    // make the operator
    auto scale = multiply_t::create("scale");
    // wire it
    scale->op1(scalar);
    scale->op2(tile);
    scale->result(result);

    // go through the cells of the result
    for (auto value : result->read()) {
        // and check them
        assert((value == 6));
    }

    // change the value of the constant
    constant->value(5);
    // and check that the result follows
    for (auto value : result->read()) {
        // one cell at a time
        assert((value == 10));
    }

    // all done
    return 0;
}


// end of file
