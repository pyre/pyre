// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the index under test
using index_t = pyre::grid::index_t<4>;


// exercise the {fill} factory, which sets every coordinate to a single value
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_fill");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // a value known while compiling
    constexpr index_t::value_type u = 42;
    // stamped on every coordinate
    constexpr index_t idx_1 = index_t::fill(u);
    // show me
    channel << "idx_1: " << idx_1 << pyre::journal::endl(__HERE__);
    // the first coordinate got the value
    static_assert(idx_1[0] == u);
    // and so did the rest
    static_assert(idx_1[1] == u);
    static_assert(idx_1[2] == u);
    static_assert(idx_1[3] == u);

    // again, with a value not known until the test runs
    index_t::value_type v = argc;
    // stamped on every coordinate
    const index_t idx_2 = index_t::fill(v);
    // show me
    channel << "idx_2: " << idx_2 << pyre::journal::endl(__HERE__);
    // the first coordinate got the value
    assert((idx_2[0] == v));
    // and so did the rest
    assert((idx_2[1] == v));
    assert((idx_2[2] == v));
    assert((idx_2[3] == v));

    // the degenerate fills coincide with their named factories
    static_assert(index_t::fill(0) == index_t::zero());
    static_assert(index_t::fill(1) == index_t::one());

    // all done
    return 0;
}


// end of file
