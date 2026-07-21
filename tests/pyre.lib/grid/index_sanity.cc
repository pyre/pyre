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


// sanity check
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // the rank is carried by the type, so it is available without an instance
    static_assert(index_t::rank() == 4);

    // make a default index
    constexpr index_t dflt {};
    // show me
    channel << "default: " << dflt << pyre::journal::endl(__HERE__);
    // the default index sits at the origin
    static_assert(dflt == index_t::zero());

    // place an index at a distinct coordinate on each axis
    constexpr index_t idx { 0, 1, 2, 3 };
    // show me
    channel << "idx: " << idx << pyre::journal::endl(__HERE__);

    // indexed access reaches the first coordinate
    static_assert(idx[0] == 0);
    // and each of the ones that follow, in order
    static_assert(idx[1] == 1);
    static_assert(idx[2] == 2);
    static_assert(idx[3] == 3);

    // the coordinate nearest the origin is reported correctly
    static_assert(idx.min() == 0);
    // as is the one furthest from it
    static_assert(idx.max() == 3);

    // coordinates are signed, so an index may sit below the origin
    constexpr index_t negative { -1, -2, -3, -4 };
    // show me
    channel << "negative: " << negative << pyre::journal::endl(__HERE__);
    // the sign survives the trip through the container
    static_assert(negative[0] == -1);
    // and the extremal coordinate is the most negative one
    static_assert(negative.min() == -4);

    // all done
    return 0;
}


// end of file
