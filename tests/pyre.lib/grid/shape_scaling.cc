// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the shape under test
using shape_t = pyre::grid::shape_t<2>;


// exercise scaling a shape by a scalar
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("shape_scaling");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // a base extent
    constexpr shape_t base { 128, 128 };
    // and a margin to grow it by
    constexpr shape_t margin { 32, 32 };

    // scaling and addition combine to enlarge the shape by two margins
    constexpr shape_t grown = base + 2 * margin;
    // show me
    channel << "base: " << base << pyre::journal::newline << "margin: " << margin
            << pyre::journal::newline << "grown: " << grown << pyre::journal::endl(__HERE__);

    // each axis grew by twice the margin
    for (shape_t::size_type axis = 0; axis < shape_t::rank(); ++axis) {
        // as scalar scaling multiplies every extent alike
        assert((grown[axis] == base[axis] + 2 * margin[axis]));
    }

    // scaling is commutative and type preserving
    static_assert(2 * margin == margin * 2);
    static_assert(std::is_same_v<decltype(margin * 2), shape_t>);
    // and dividing undoes multiplying by the same factor
    static_assert((margin * 2) / 2 == margin);

    // all done
    return 0;
}


// end of file
