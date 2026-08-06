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


// exercise the row major factory
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("order_c");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.order");

    // the c convention packs the trailing axis fastest
    constexpr order_t rowMajor = order_t::c();
    // show me
    channel << pyre::journal::at() << "row major: " << rowMajor << pyre::journal::endl;

    // so it names the last axis first and the first axis last
    static_assert(rowMajor[0] == 3);
    static_assert(rowMajor[1] == 2);
    static_assert(rowMajor[2] == 1);
    static_assert(rowMajor[3] == 0);

    // which is a genuine permutation of the axis labels
    static_assert(rowMajor.isPermutation());

    // all done
    return 0;
}


// end of file
