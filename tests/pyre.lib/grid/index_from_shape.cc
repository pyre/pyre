// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the types under test
using index_t = pyre::grid::index_t<2>;
using shape_t = pyre::grid::shape_t<2>;


// exercise the constructor that reads the extents of a shape as coordinates
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("index_from_shape");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // make a shape
    constexpr shape_t shape { 3, 5 };
    // read its extents as coordinates
    constexpr index_t idx { shape };
    // show me
    channel << pyre::journal::at() << "idx: " << idx << pyre::journal::endl;
    // the extents survive the trip
    static_assert(idx[0] == 3);
    static_assert(idx[1] == 5);

    // the motivating use: anchor a grid so the shape is centered at the origin
    constexpr index_t origin { -shape / 2 };
    // show me
    channel << pyre::journal::at() << "origin: " << origin << pyre::journal::endl;
    // the coordinates reflect the halved extents, mirrored through the origin
    static_assert(origin[0] == -1);
    static_assert(origin[1] == -2);
    // and displacing the origin by the shape steps past the far corner
    static_assert((origin + shape) == index_t { 2, 3 });

    // all done
    return 0;
}


// end of file
