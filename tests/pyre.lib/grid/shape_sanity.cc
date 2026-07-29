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
using shape_t = pyre::grid::shape_t<4>;


// sanity check
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("shape_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // the rank is carried by the type, so it is available without an instance
    static_assert(shape_t::rank() == 4);

    // lay out a shape with a distinct extent on each axis
    constexpr shape_t shape { 2, 3, 4, 5 };
    // show me
    channel << pyre::journal::at() << "shape: " << shape << pyre::journal::endl;

    // indexed access reaches the first axis
    static_assert(shape[0] == 2);
    // and each of the ones that follow, in order
    static_assert(shape[1] == 3);
    static_assert(shape[2] == 4);
    static_assert(shape[3] == 5);

    // the number of addressable cells is the product of the extents
    static_assert(shape.cells() == 2 * 3 * 4 * 5);

    // the shortest axis is reported correctly
    static_assert(shape.min() == 2);
    // as is the longest
    static_assert(shape.max() == 5);

    // all done
    return 0;
}


// end of file
