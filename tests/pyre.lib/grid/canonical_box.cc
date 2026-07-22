// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the packing strategy under test, at a rank high enough to exercise several axes at once
using canonical_t = pyre::grid::canonical_t<6>;
// and its parts
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;


// verify that a sub-box inherits the physical layout of the strategy it was cut from
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("canonical_box");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // pick a shape with coprime extents, so a stray stride cannot go unnoticed
    constexpr shape_t shape { 3, 5, 7, 11, 13, 17 };
    // lay it out in column major order
    constexpr canonical_t packing { shape, index_t {}, canonical_t::order_type::fortran() };

    // carve out a sub-box anchored inside the parent
    constexpr index_t base { 1, 2, 4, 5, 6, 7 };
    // with an extent that leaves room on every axis
    constexpr shape_t tile { 1, 1, 2, 1, 4, 1 };
    // extract it
    constexpr auto box = packing.box(base, tile);
    // show me
    channel << "box shape: " << box.shape() << pyre::journal::newline
            << "box origin: " << box.origin() << pyre::journal::newline
            << "box strides: " << box.strides() << pyre::journal::endl(__HERE__);

    // the box reports the extent it was asked for
    static_assert(box.shape() == tile);
    // and is anchored where we placed it
    static_assert(box.origin() == base);
    // and it keeps the parent's physical strides, which is what makes it address parent memory
    static_assert(box.strides() == packing.strides());

    // its traversal starts at the anchor
    assert((*box.begin() == base));
    // and ends one past the far corner
    assert((*box.end() == base + tile));

    // every index of the box resolves to the same offset in the box and in its parent
    for (auto it = box.begin(); it != box.end(); ++it) {
        // name the cell
        auto idx = *it;
        // show me
        channel << pyre::journal::at() << "  " << idx << " -> " << box.offset(idx)
                << pyre::journal::newline;
        // the sub-box addresses the very cell the parent does
        assert((box.offset(idx) == packing.offset(idx)));
    }
    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
