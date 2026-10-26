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
// the sum of two tiles
using add_t = pyre::flow::factories::operators::add_t<tile_t>;
// their difference
using subtract_t = pyre::flow::factories::operators::subtract_t<tile_t>;
// the product of a scalar and a tile
using multiply_t = pyre::flow::factories::operators::multiply_t<scalar_t, tile_t>;
// and the quotient of a tile by a scalar
using divide_t = pyre::flow::factories::operators::divide_t<tile_t, scalar_t>;

// driver: the operators spell their types the way the catalog and the recipes expect
int
main(int argc, char * argv[])
{
    // the spelling of the scalars
    assert(scalar_t::declSelf() == "pyre::flow::products::var_t<double>");
    // and their human readable name
    assert(scalar_t::className() == "VariableDouble");

    // the spelling of the sum of two tiles names its alias and its products
    assert(
        add_t::declSelf()
        == "pyre::flow::factories::operators::add_t<" + tile_t::declSelf() + ", "
               + tile_t::declSelf() + ", " + tile_t::declSelf() + ">");
    // and so does the difference
    assert(
        subtract_t::declSelf()
        == "pyre::flow::factories::operators::subtract_t<" + tile_t::declSelf() + ", "
               + tile_t::declSelf() + ", " + tile_t::declSelf() + ">");
    // the product of a scalar and a tile
    assert(
        multiply_t::declSelf()
        == "pyre::flow::factories::operators::multiply_t<" + scalar_t::declSelf() + ", "
               + tile_t::declSelf() + ", " + tile_t::declSelf() + ">");
    // and the quotient of a tile by a scalar
    assert(
        divide_t::declSelf()
        == "pyre::flow::factories::operators::divide_t<" + tile_t::declSelf() + ", "
               + scalar_t::declSelf() + ", " + tile_t::declSelf() + ">");

    // the human readable names
    assert(add_t::className() == "Add");
    assert(subtract_t::className() == "Subtract");
    assert(multiply_t::className() == "Multiply");
    assert(divide_t::className() == "Divide");

    // the slots
    const auto & slots = add_t::declSlots();
    // are three
    assert(slots.size() == 3);
    // the operands
    assert(slots[0].name() == "op1" && slots[0].reads());
    assert(slots[1].name() == "op2" && slots[1].reads());
    // and the result
    assert(slots[2].name() == "result" && slots[2].writes());

    // all done
    return 0;
}


// end of file
