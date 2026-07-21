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


// exercise scaling an index by a scalar
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_scaling");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // a reference corner
    constexpr index_t ref { 128, 128 };
    // and a margin to grow it by
    constexpr index_t margin { 32, 32 };

    // scaling and addition combine to place a second corner two margins out
    constexpr index_t sec = ref + 2 * margin;
    // show me
    channel << "ref: " << ref << pyre::journal::newline << "margin: " << margin
            << pyre::journal::newline << "sec: " << sec << pyre::journal::endl(__HERE__);

    // each axis grew by twice the margin
    for (index_t::size_type axis = 0; axis < index_t::rank(); ++axis) {
        // as scalar scaling multiplies every coordinate alike
        assert((sec[axis] == ref[axis] + 2 * margin[axis]));
    }

    // scaling is commutative: the scalar may sit on either side
    static_assert(2 * margin == margin * 2);
    // and it preserves the index type
    static_assert(std::is_same_v<decltype(margin * 2), index_t>);
    // dividing undoes multiplying by the same factor
    static_assert((margin * 2) / 2 == margin);

    // all done
    return 0;
}


// end of file
