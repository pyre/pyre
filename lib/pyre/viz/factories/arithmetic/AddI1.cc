// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// externals
#include "../external.h"
// forward declarations
#include "../forward.h"
// type aliases
#include "../api.h"

// my class declaration
#include "AddI1.h"
// my product type
#include "../../products/memory/I1.h"

// destructor
pyre::viz::factories::arithmetic::AddI1::~AddI1()
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz.factories.arithmetic.addi1");
    // let me know
    channel
        // mark
        << "addi1 '" << name() << "' at " << this << ": destroy"
        << pyre::journal::newline
        // flush
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}

// accessors
auto
pyre::viz::factories::arithmetic::AddI1::op1() -> product_ref_type
{
    // look up the product bound to {op1} and return it
    return std::dynamic_pointer_cast<product_type>(input("op1"));
}

auto
pyre::viz::factories::arithmetic::AddI1::op2() -> product_ref_type
{
    // look up the product bound to {op2} and return it
    return std::dynamic_pointer_cast<product_type>(input("op2"));
}

auto
pyre::viz::factories::arithmetic::AddI1::result() -> product_ref_type
{
    // look up the product bound to {result} and return it
    return std::dynamic_pointer_cast<product_type>(output("result"));
}

// mutators
auto
pyre::viz::factories::arithmetic::AddI1::op1(product_ref_type arg) -> factory_ref_type
{
    // connect my {op1} slot
    addInput("op1", std::static_pointer_cast<pyre::flow::product_t>(arg));
    // make a self reference
    auto self = std::dynamic_pointer_cast<AddI1>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::arithmetic::AddI1::op2(product_ref_type arg) -> factory_ref_type
{
    // connect my {op2} slot
    addInput("op2", std::static_pointer_cast<pyre::flow::product_t>(arg));
    // make a self reference
    auto self = std::dynamic_pointer_cast<AddI1>(ref());
    // and return it
    return self;
}

auto
pyre::viz::factories::arithmetic::AddI1::result(product_ref_type arg) -> factory_ref_type
{
    // connect my {result} slot
    addOutput("result", std::static_pointer_cast<pyre::flow::product_t>(arg));
    // make a self reference
    auto self = std::dynamic_pointer_cast<AddI1>(ref());
    // and return it
    return self;
}

// interface
auto
pyre::viz::factories::arithmetic::AddI1::make(
    const name_type & slot, base_type::product_ref_type product) -> base_type::factory_ref_type
{
    // chain up
    auto self = base_type::make(slot, product);
    // compute the value
    auto value = op1()->read() + op2()->read();
    // and save it
    result()->write(value);
    // all done
    return self;
}

// end of file
