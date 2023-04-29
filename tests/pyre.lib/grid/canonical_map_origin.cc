// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using canonical_t = pyre::grid::canonical_t<3>;


// simple check that the map to and from index space is correct in the presence of a
// non-trivial origin
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("canonical_map_origin");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // pick a shape
    canonical_t::shape_type shape { 3, 5, 7 };
    // the indices range from (-1, -2)  to (1, 2)
    canonical_t::index_type origin { -1, 0, 0 };
    // and the cells are in c mode (the default)
    auto order = canonical_t::order_type::c();
    // assemble a canonical packing strategy
    canonical_t packing { shape, origin, order };

    // verify that the offset of the {origin} is zero
    assert(( packing.offset(origin) == 0 ));
    // verify that the offset of {0,0,0}
    canonical_t::index_type zero {};
    // is equal to the nudge
    assert(( packing.offset(zero) == packing.nudge() ));

    // make an index
    canonical_t::index_type index { 1, 2, 3 };
    // get its offset
    auto offset = packing.offset(index);
    // map it back to an index
    auto image = packing.index(offset);

    // show me
    channel
        << "shape: " << packing.shape() << pyre::journal::newline
        << "origin: " << packing.origin() << pyre::journal::newline
        << "order: " << packing.order() << pyre::journal::newline
        << "strides: " << packing.strides() << pyre::journal::newline
        << "nudge: " << packing.nudge() << pyre::journal::newline
        << "begin: " << *packing.begin() << pyre::journal::newline
        << "end: " << *packing.end() << pyre::journal::newline
        << "index: " << index << pyre::journal::newline
        << "offset: " << offset << pyre::journal::newline
        << "image: " << image << pyre::journal::endl(__HERE__);

    // verify that the {image} is our original index
    assert(( image == index ));

    // all done
    return 0;
}


// end of file
