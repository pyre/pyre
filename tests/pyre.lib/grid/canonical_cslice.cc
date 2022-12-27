// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using canonical_t = pyre::grid::canonical_t<6>;


// simple check that the map from index space to offsets is correct
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("canonical_cslice");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // pick a shape
    canonical_t::shape_type shape { 3, 5, 7, 11, 13, 17 };
    // an origin
    canonical_t::index_type origin {};
    // and a packing order
    auto order = canonical_t::order_type::fortran();
    // make a canonical packing strategy
    canonical_t packing { shape, origin, order };
    // show me
    channel
        << "packing:" << pyre::journal::newline
        << "    shape: " << packing.shape() << pyre::journal::newline
        << "    origin: " << packing.origin() << pyre::journal::newline
        << "    order: " << packing.order() << pyre::journal::newline
        << "    strides: " << packing.strides() << pyre::journal::newline
        << "    cells: " << packing.cells() << pyre::journal::newline
        << "    nudge: " << packing.nudge() << pyre::journal::endl(__HERE__);

    // find a spot
    canonical_t::index_type spot {1,2,4,5,6,7};
    // extract a slice
    auto slice = packing.cslice<0,0,2,0,4,0>(spot);
    // show me
    channel
        << "slice:" << pyre::journal::newline
        << "    base: " << spot << pyre::journal::newline
        << "    shape: " << slice.shape() << pyre::journal::newline
        << "    origin: " << slice.origin() << pyre::journal::newline
        << "    order: " << slice.order() << pyre::journal::newline
        << "    strides: " << slice.strides() << pyre::journal::newline
        << "    cells: " << slice.cells() << pyre::journal::newline
        << "    nudge: " << slice.nudge() << pyre::journal::endl(__HERE__);

    // verify the slice offsets
    assert(( slice[{0,0}] == packing[{1,2,4,5,6,7}] ));
    assert(( slice[{0,1}] == packing[{1,2,4,5,7,7}] ));
    assert(( slice[{0,2}] == packing[{1,2,4,5,8,7}] ));
    assert(( slice[{0,3}] == packing[{1,2,4,5,9,7}] ));
    assert(( slice[{1,0}] == packing[{1,2,5,5,6,7}] ));
    assert(( slice[{1,1}] == packing[{1,2,5,5,7,7}] ));
    assert(( slice[{1,2}] == packing[{1,2,5,5,8,7}] ));
    assert(( slice[{1,3}] == packing[{1,2,5,5,9,7}] ));

    // all done
    return 0;
}


// end of file
