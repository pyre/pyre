// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <tuple>
// get the grid
#include <pyre/grid.h>


// the index under test
using index_t = pyre::grid::index_t<4>;


// spread a tuple of coordinates across the index constructor
auto convert = [](auto && tuple) {
    // a helper that forwards its arguments into an index
    constexpr auto build = [](auto &&... x) {
        // one coordinate per tuple element
        return index_t { std::forward<decltype(x)>(x)... };
    };
    // apply it to the tuple
    return std::apply(build, tuple);
};


// verify that an index can be assembled from a tuple of coordinates
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_from_tuple");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // a tuple carrying the coordinates in order
    auto src = std::make_tuple(0, 1, 2, 3);
    // spread across the index constructor
    auto idx = convert(src);
    // show me
    channel << "idx: " << idx << pyre::journal::endl(__HERE__);

    // the coordinates arrive in the order the tuple held them
    assert((idx == index_t { 0, 1, 2, 3 }));

    // all done
    return 0;
}


// end of file
