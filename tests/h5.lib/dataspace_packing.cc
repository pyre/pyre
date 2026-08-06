// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the h5 support
#include <pyre/h5.h>


// verify that a dataspace can describe its extent in the {pyre::grid} vocabulary, and that
// extents compare through {sameExtent}
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataspace_packing");

    // make a simple dataspace
    pyre::h5::DataSpace space { pyre::h5::shape_t { 4, 6 } };

    // ask it to speak grid
    auto packing = space.packing();
    // the rank crosses over
    assert((packing.rank() == 2));
    // so does the extent, now in signed coordinates
    assert((packing.shape() == pyre::h5::packing_t::shape_type { 4, 6 }));
    // the box is anchored at zero
    assert((packing.origin() == pyre::h5::packing_t::index_type { 0, 0 }));
    // it packs every cell
    assert((packing.cells() == 4 * 6));
    // and the strides follow the c convention, with the last index varying fastest
    assert((packing.strides() == pyre::h5::packing_t::strides_type { 6, 1 }));

    // a clone has the same extent
    assert((space.sameExtent(space.clone())));
    // a dataspace of a different shape does not
    assert((!space.sameExtent(pyre::h5::DataSpace { pyre::h5::shape_t { 4, 7 } })));
    // and neither does one of a different rank
    assert((!space.sameExtent(pyre::h5::DataSpace { pyre::h5::shape_t { 4, 6, 1 } })));

    // all done
    return 0;
}


// end of file
