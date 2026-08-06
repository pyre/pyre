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


// exercise walking the coordinates of a single index
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_iterator");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // an index whose coordinates run in step with the axis number
    constexpr index_t idx { 0, 1, 2, 3 };
    // show me
    channel << pyre::journal::at() << "idx: " << idx << pyre::journal::endl;

    // the count of coordinates seen so far doubles as the value each one should hold
    index_t::value_type expected = 0;
    // an index hands out the iterators of its backing store, so a range based {for} visits its
    // coordinates from the first axis to the last
    for (auto coordinate : idx) {
        // each coordinate is the axis number
        assert((coordinate == expected));
        // ready for the next axis
        ++expected;
    }
    // the walk must have visited every axis
    assert((expected == index_t::rank()));

    // all done
    return 0;
}


// end of file
