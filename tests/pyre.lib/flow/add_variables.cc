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
// the products
using product_t = pyre::flow::products::var_t<cell_t>;
// build the operator
using factory_t = pyre::flow::factories::add_variables_t<cell_t>;

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
    // make the result
    auto result = product_t::create("result", 0);

    // make the operator
    auto add = factory_t::create("add");
    // wire the workflow
    add->op1(op1);
    add->op2(op2);
    add->result(result);

    // get the bindings
    const auto & inputs = add->inputs();
    const auto & outputs = add->outputs();
    // verify the factory arity
    assert((inputs.size() == 2));
    assert((outputs.size() == 1));
    // and the slot contents
    assert(inputs.find("op1")->second == op1);
    assert(inputs.find("op2")->second == op2);
    assert(outputs.find("result")->second == result);

    // check the value
    assert(result->read() == 3);

    // update one of the operands
    op1->value(3);
    // and check the value again
    assert(result->read() == 5);

    // all done
    return 0;
}

// end of file