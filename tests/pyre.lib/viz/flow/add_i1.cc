// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>


// type aliases
using product_t = pyre::viz::products::memory::i1_t;
using factory_t = pyre::viz::factories::arithmetic::add_i1_t;

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
    // check the initial values
    assert(op1->value() == 1);
    assert(op2->value() == 2);
    assert(result->value() == 0);

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
    assert((value == 3));

    // update one of the operands
    op1->value(3);
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
    assert((value == 5));

    // all done
    return 0;
}

// end of file