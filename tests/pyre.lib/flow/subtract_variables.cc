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
// the scalars
using scalar_t = pyre::flow::products::var_t<cell_t>;
// the operator
using factory_t = pyre::flow::factories::operators::subtract_t<scalar_t>;

// driver: subtracting a scalar from another respects the order
int
main(int argc, char * argv[])
{
    // make the operands
    auto op1 = scalar_t::create("op1", 5);
    auto op2 = scalar_t::create("op2", 2);
    // and the result
    auto result = scalar_t::create("result", 0);

    // make the operator
    auto subtract = factory_t::create("subtract");
    // wire it
    subtract->op1(op1);
    subtract->op2(op2);
    subtract->result(result);

    // check the result
    assert((result->read() == 3));

    // update the first operand
    op1->value(1);
    // and check that the result follows
    assert((result->read() == -1));

    // all done
    return 0;
}


// end of file
