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
using shape_t = pyre::grid::shape_t<3>;


// exercise structured binding support
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("shape_structured_binding");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // a shape with distinct extents
    shape_t shape { 10, 20, 30 };
    // which structured binding pulls apart into one name per axis
    auto [nx, ny, nz] = shape;
    // show me
    channel << "shape: " << shape << pyre::journal::newline << "unpacked: " << nx << ", " << ny
            << ", " << nz << pyre::journal::endl(__HERE__);

    // each name is the extent of its axis
    assert((nx == shape[0]));
    assert((ny == shape[1]));
    assert((nz == shape[2]));

    // binding by reference reaches the extents in place, so a write lands back in the shape
    auto & [rx, ry, rz] = shape;
    // resize the middle axis
    ry = 99;
    // and the shape sees it
    assert((shape[1] == 99));

    // the tuple protocol reports the rank as the number of names to unpack
    static_assert(std::tuple_size_v<shape_t> == 3);

    // all done
    return 0;
}


// end of file
