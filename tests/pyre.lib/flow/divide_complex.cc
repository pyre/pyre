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
using cell_t = std::complex<double>;
// a packing
using packing_t = pyre::grid::canonical_t<2>;
// and a storage strategy
using storage_t = pyre::memory::heap_t<cell_t>;
// use them to make a grid
using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
// the tiles
using tile_t = pyre::flow::products::tile_t<grid_t>;
// and the scalars
using scalar_t = pyre::flow::products::var_t<double>;
// the operator
using factory_t = pyre::flow::factories::operators::divide_t<tile_t, scalar_t>;

// driver: dividing a tile of complex numbers by a real scalar scales both parts of every cell
int
main(int argc, char * argv[])
{
    // pick a shape
    auto shape = tile_t::shape_type(8, 8);
    // make the tile
    auto tile = tile_t::create("tile", shape, cell_t(2, -4));
    // and the scalar
    auto scalar = scalar_t::create("scalar", 2);
    // and the result
    auto result = tile_t::create("result", shape, 0);

    // make the operator
    auto divide = factory_t::create("divide");
    // wire it
    divide->op1(tile);
    divide->op2(scalar);
    divide->result(result);

    // go through the cells of the result
    for (auto value : result->read()) {
        // and check them
        assert((value == cell_t(1, -2)));
    }

    // all done
    return 0;
}


// end of file
