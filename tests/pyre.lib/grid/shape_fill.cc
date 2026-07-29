// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the shape under test
using shape_t = pyre::grid::shape_t<4>;


// exercise the {fill} factory
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("shape_fill");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // pick an extent that is known while compiling
    constexpr shape_t::value_type u = 42;
    // stamp it on every axis
    constexpr shape_t shape_1 = shape_t::fill(u);
    // show me
    channel << pyre::journal::at() << "shape_1: " << shape_1 << pyre::journal::endl;
    // the first axis got the requested extent
    static_assert(shape_1[0] == u);
    // and so did every other one
    static_assert(shape_1[1] == u);
    static_assert(shape_1[2] == u);
    static_assert(shape_1[3] == u);

    // again, with an extent that cannot be known until the test runs
    shape_t::value_type v = argc;
    // stamp it on every axis
    const shape_t shape_2 = shape_t::fill(v);
    // show me
    channel << pyre::journal::at() << "shape_2: " << shape_2 << pyre::journal::endl;
    // the first axis got the requested extent
    assert((shape_2[0] == v));
    // and so did every other one
    assert((shape_2[1] == v));
    assert((shape_2[2] == v));
    assert((shape_2[3] == v));

    // the degenerate fill has a factory of its own
    static_assert(shape_t::fill(0) == shape_t::zero());
    // as does the unit fill
    static_assert(shape_t::fill(1) == shape_t::one());

    // all done
    return 0;
}


// end of file
