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

    // read the value
    int value = result->value();
    // show me
    channel
        // the value
        << "add: value=" << value
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);
    // check it
    assert((value == 6));

    // update one of the operands
    op1->value(4);
    // again, read the value
    value = result->value();
    // show me
    channel
        // the value
        << "add: value=" << value
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);
    // check it gain
    assert((value == 9));

    // all done
    return 0;
}

// end of file