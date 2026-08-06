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
using index_t = pyre::grid::index_t<3>;


// exercise structured binding support
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_structured_binding");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // an index with distinct coordinates
    index_t idx { 10, 20, 30 };
    // which structured binding pulls apart into one name per axis
    auto [x, y, z] = idx;
    // show me
    channel << pyre::journal::at() << "idx: " << idx << pyre::journal::newline << "unpacked: " << x
            << ", " << y << ", " << z << pyre::journal::endl;

    // each name is the coordinate of its axis
    assert((x == idx[0]));
    assert((y == idx[1]));
    assert((z == idx[2]));

    // binding by reference reaches the coordinates in place, so a write lands back in the index
    auto & [a, b, c] = idx;
    // move the middle axis
    b = 99;
    // and the index sees it
    assert((idx[1] == 99));

    // the tuple protocol reports the rank as the number of names to unpack
    static_assert(std::tuple_size_v<index_t> == 3);

    // all done
    return 0;
}


// end of file
