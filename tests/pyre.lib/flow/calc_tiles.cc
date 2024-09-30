// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


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
// the products
using product_t = pyre::flow::products::tile_t<grid_t>;
// build the operator
using factory_t = pyre::flow::factories::add_tiles_t<grid_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow");
    // turn it on
    // channel.activate();

    // make the operands
    auto op1 = product_t::create("op1", 1);
    auto op2 = product_t::create("op2", 2);
    auto op3 = product_t::create("op3", 3);
    // the intermediate
    auto tmp = product_t::create("tmp", 0);
    // and the result
    auto result = product_t::create("result", 0);

    // make the first operator
    auto add1 = factory_t::create("add1");
    // wire it
    add1->op1(op1);
    add1->op2(op2);
    add1->result(tmp);
    // make the second operator
    auto add2 = factory_t::create("add2");
    // wire it
    add2->op1(tmp);
    add2->op2(op3);
    add2->result(result);

    // go through the cells in result
    for (auto value : result->read()) {
        // and check the value
        assert((value == 6));
    }

    // update one of the operands
    op1->value(4);
    // go through the cells in result
    for (auto value : result->read()) {
        // and check the value
        assert((value == 9));
    }

    // all done
    return 0;
}

// end of file