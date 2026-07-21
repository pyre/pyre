// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the packing strategy under test
using canonical_t = pyre::grid::canonical_t<3>;
// and its parts
using shape_t = canonical_t::shape_type;
using index_t = canonical_t::index_type;
// the hyperplane that keeps two axes is a rank two layout
using plane_t = pyre::grid::canonical_t<2>;


// verify that a hyperplane inherits the physical layout of the strategy it was cut from
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("canonical_slice");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // pick a shape
    constexpr shape_t shape { 2, 3, 4 };
    // lay it out canonically
    constexpr canonical_t packing { shape };

    // keep axes 0 and 2, pinning axis 1 at 1
    constexpr auto plane = packing.slice<0, 2>(index_t { 0, 1, 0 });
    // show me
    channel << "plane shape: " << plane.shape() << pyre::journal::newline
            << "plane strides: " << plane.strides() << pyre::journal::endl(__HERE__);

    // the surviving axes keep their extents, in the order they were named
    static_assert(plane.shape() == plane_t::shape_type { 2, 4 });
    // and their physical strides, so the plane addresses the parent's cells
    static_assert(plane.strides()[0] == packing.strides()[0]);
    static_assert(plane.strides()[1] == packing.strides()[2]);

    // every cell of the plane resolves to the same offset as the full index that names it in the
    // parent, with the pinned axis restored
    for (canonical_t::difference_type i = 0; i < 2; ++i) {
        // sweep the second surviving axis too
        for (canonical_t::difference_type k = 0; k < 4; ++k) {
            // the cell in the plane's own index space
            auto flat = plane_t::index_type { i, k };
            // and the same cell in the parent's, with axis 1 put back
            auto full = index_t { i, 1, k };
            // show me
            channel << pyre::journal::at() << "  " << flat << " -> " << plane.offset(flat)
                    << pyre::journal::newline;
            // the two routes must arrive at the same offset
            assert((plane.offset(flat) == packing.offset(full)));
        }
    }
    // flush the trace
    channel << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
