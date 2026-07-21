// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/_grid_.h>


// the index under test
using index_t = pyre::grid::index_t<4>;


// exercise indexed read and write
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_access");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // a compile time index reads back the coordinates it was built from
    constexpr index_t known { 0, 1, 2, 3 };
    // show me
    channel << "known: " << known << pyre::journal::endl(__HERE__);
    // each coordinate is where it was placed
    static_assert(known[0] == 0);
    static_assert(known[1] == 1);
    static_assert(known[2] == 2);
    static_assert(known[3] == 3);

    // a mutable index starts out at the origin
    index_t scratch {};
    // and each coordinate can be written through the subscript
    scratch[0] = 0;
    scratch[1] = 1;
    scratch[2] = 2;
    scratch[3] = 3;
    // show me
    channel << "scratch: " << scratch << pyre::journal::endl(__HERE__);
    // the writes must be visible on read back
    assert((scratch == known));

    // all done
    return 0;
}


// end of file
