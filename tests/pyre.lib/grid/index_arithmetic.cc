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
using index_t = pyre::grid::index_t<2>;


// exercise component-wise index arithmetic
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_arithmetic");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // a reference corner
    constexpr index_t ref { 128, 128 };
    // and a second one further out
    constexpr index_t sec { 192, 192 };

    // the span from one to the other, counting both endpoints
    constexpr index_t span = sec - ref + index_t::one();
    // show me
    channel << pyre::journal::at() << "ref: " << ref << pyre::journal::newline << "sec: " << sec
            << pyre::journal::newline << "span: " << span << pyre::journal::endl;

    // each axis reports its own span
    for (index_t::size_type axis = 0; axis < index_t::rank(); ++axis) {
        // which is the difference of the endpoints, plus one for the fence post
        assert((span[axis] == sec[axis] - ref[axis] + 1));
    }

    // the result is type preserving: subtracting and adding indices yields an index
    static_assert(std::is_same_v<decltype(sec - ref), index_t>);

    // negation reflects every coordinate through the origin
    static_assert(-ref == index_t { -128, -128 });

    // all done
    return 0;
}


// end of file
