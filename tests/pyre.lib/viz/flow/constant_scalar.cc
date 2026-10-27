// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a constant sets the scalar bound to its {result}, and sets it again when its value
// changes


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/journal.h>
#include <pyre/viz.h>


// type aliases
using scalar_t = pyre::flow::products::var_t<double>;
using constant_t = pyre::flow::factories::filters::constant_t<scalar_t>;


// driver
int
main(int argc, char * argv[])
{
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.viz");
    // turn it on
    // channel.activate();

    // make a scalar
    auto scalar = scalar_t::create("scalar");
    // pick a value
    auto value = 3.5;
    // make the factory
    auto constant = constant_t::create("constant", value);
    // wire it
    constant->result(scalar);
    // check that the scalar holds the value
    assert((scalar->read() == value));

    // pick another value
    value = -2;
    // modify the factory
    constant->value(value);
    // check that the scalar reflects the new value
    assert((scalar->read() == value));

    // all done
    return 0;
}


// end of file
