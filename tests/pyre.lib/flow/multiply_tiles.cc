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
using factory_t = pyre::flow::factories::multiply_tiles_t<grid_t>;

// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.flow");
    // turn it on
    // channel.activate();

    // pick a shape
    auto shape = product_t::shape_type(512, 512);
    // make the operands
    auto op1 = product_t::create("op1", shape, 1);
    auto op2 = product_t::create("op2", shape, 2);
    // make the result
    auto result = product_t::create("result", shape, 0);

    // make the operator
    auto multiply = factory_t::create("multiply");
    // wire the workflow
    multiply->op1(op1);
    multiply->op2(op2);
    multiply->result(result);

    // get the bindings
    const auto & inputs = multiply->inputs();
    const auto & outputs = multiply->outputs();
    // verify the factory arity
    assert((inputs.size() == 2));
    assert((outputs.size() == 1));
    // and the slot contents
    assert(inputs.find("op1")->second == op1);
    assert(inputs.find("op2")->second == op2);
    assert(outputs.find("result")->second == result);

    // go through the cells in result
    for (auto value : result->read()) {
        // and check the value
        assert((value == 2));
    }

    // update one of the operands
    op1->value(3);
    // again,  go through the cells in result
    for (auto value : result->read()) {
        // and check the value
        assert((value == 6));
    }

    // all done
    return 0;
}

// end of file