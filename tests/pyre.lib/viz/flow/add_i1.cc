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
    channel.activate();

    // make the operands
    auto op1 = product_t::create(1);
    auto op2 = product_t::create(2);
    // make the result
    auto result = product_t::create(0);
    // make the operator
    auto add = factory_t::create();

    // connect them
    add->op1(op1);
    add->op2(op2);
    add->result(result);

    // read the value
    int value = result->read();
    // show me
    channel
        // the value
        << "add: value=" << value
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);

    // again, read the value
    value = result->read();
    // show me
    channel
        // the value
        << "add: value=" << value
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}

// end of file