// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <numeric>
// get the grid
#include <pyre/grid.h>


// the packing strategy under test
using canonical_t = pyre::grid::canonical_t<3>;


// verify that {offset} is the inner product of the index with the strides
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("canonical_offset");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // pick extents large enough that their products overrun a 32 bit integer; a signed cell
    // type is exactly what lets these offsets stay correct
    constexpr canonical_t::shape_type shape { 1 << 12, 1 << 12, 1 << 12 };
    // lay it out canonically at the origin
    constexpr canonical_t packing { shape };
    // show me
    channel << "shape: " << packing.shape() << pyre::journal::newline
            << "strides: " << packing.strides() << pyre::journal::newline
            << "cells: " << packing.cells() << pyre::journal::endl(__HERE__);

    // with the origin at zero, the first cell sits at offset zero
    static_assert(packing.nudge() == 0);
    static_assert(packing.offset({ 0, 0, 0 }) == 0);

    // the far corner of the box
    constexpr auto corner = canonical_t::index_type::fill((1 << 12) - 1);
    // its offset is the inner product of its coordinates with the strides
    auto expected = std::inner_product(
        corner.begin(), corner.end(), packing.strides().begin(),
        canonical_t::difference_type { 0 });
    // show me
    channel << "corner: " << corner << pyre::journal::newline
            << "offset: " << packing.offset(corner) << pyre::journal::newline
            << "inner product: " << expected << pyre::journal::endl(__HERE__);
    // the two must agree, and neither may have wrapped
    assert((packing.offset(corner) == expected));
    // the corner is the last addressable cell, so its offset is one short of the cell count
    assert((packing.offset(corner) == packing.cells() - 1));

    // all done
    return 0;
}


// end of file
