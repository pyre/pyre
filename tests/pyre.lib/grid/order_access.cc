// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the packing order under test
using order_t = pyre::grid::order_t<4>;


// exercise indexed read and write of the axis labels
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("order_access");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.order");

    // a compile time order reads back the axis labels it was built from
    constexpr order_t known { 0, 1, 2, 3 };
    // show me
    channel << "known: " << known << pyre::journal::endl(__HERE__);
    // slot {level} names the axis that runs at that packing level
    static_assert(known[0] == 0);
    static_assert(known[1] == 1);
    static_assert(known[2] == 2);
    static_assert(known[3] == 3);

    // an order can be assembled a slot at a time; start from the row major arrangement
    order_t scratch = order_t::c();
    // then overwrite each slot with the identity permutation
    scratch[0] = 0;
    scratch[1] = 1;
    scratch[2] = 2;
    scratch[3] = 3;
    // show me
    channel << "scratch: " << scratch << pyre::journal::endl(__HERE__);
    // the writes must be visible on read back
    assert((scratch == known));
    // and the result is still a genuine permutation
    assert((scratch.isPermutation()));

    // all done
    return 0;
}


// end of file
