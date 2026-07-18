// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/_grid_.h>


// the packing strategy under test
using canonical_t = pyre::grid::canonical_t<3>;


// verify that the layout is recorded as requested
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("canonical_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // the rank is carried by the type, so it is available without an instance
    static_assert(canonical_t::rank() == 3);

    // pick a shape
    constexpr canonical_t::shape_type shape { 2, 3, 4 };
    // let the strategy deduce a tight layout over it
    constexpr canonical_t packing { shape };

    // show me
    channel << "shape: " << packing.shape() << pyre::journal::newline
            << "origin: " << packing.origin() << pyre::journal::newline
            << "order: " << packing.order() << pyre::journal::newline
            << "strides: " << packing.strides() << pyre::journal::newline
            << "nudge: " << packing.nudge() << pyre::journal::endl(__HERE__);

    // the shape is recorded verbatim
    static_assert(packing.shape() == shape);
    // absent instructions, the axes are packed in row major order
    static_assert(packing.order() == canonical_t::order_type::c());
    // and the layout is anchored at the origin
    static_assert(packing.origin() == canonical_t::index_type::zero());

    // a tight layout addresses exactly as many cells as the shape demands
    static_assert(packing.cells() == shape.cells());

    // the nudge corrects for an origin away from zero, so here there is nothing to correct
    static_assert(packing.nudge() == 0);

    // and the origin therefore lands at the beginning of the block
    static_assert(packing.offset({ 0, 0, 0 }) == 0);

    // all done
    return 0;
}


// end of file
