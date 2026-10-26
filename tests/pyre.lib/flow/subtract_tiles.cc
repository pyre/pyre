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
// the operator
using factory_t = pyre::flow::factories::operators::subtract_t<tile_t>;

// driver: subtracting a tile from another respects the order
int
main(int argc, char * argv[])
{
    // pick a shape
    auto shape = tile_t::shape_type(8, 8);
    // make the operands
    auto op1 = tile_t::create("op1", shape, 5);
    auto op2 = tile_t::create("op2", shape, 2);
    // and the result
    auto result = tile_t::create("result", shape, 0);

    // make the operator
    auto subtract = factory_t::create("subtract");
    // wire it
    subtract->op1(op1);
    subtract->op2(op2);
    subtract->result(result);

    // go through the cells of the result
    for (auto value : result->read()) {
        // and check them
        assert((value == 3));
    }

    // update the second operand
    op2->value(7);
    // and check that the result follows
    for (auto value : result->read()) {
        // one cell at a time
        assert((value == -2));
    }

    // all done
    return 0;
}


// end of file
