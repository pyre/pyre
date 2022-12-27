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


// simple check that the map from index space to offsets is correct
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("canonical_visit_order");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // pick a shape
    canonical_t::shape_type shape { 2,3,4 };
    // make a canonical packing strategy
    canonical_t packing { shape };
    // show me
    channel
        << "packing:" << pyre::journal::newline
        << "  shape: " << packing.shape() << pyre::journal::newline
        << "  order: " << packing.order() << pyre::journal::newline
        << "  origin: " << packing.order() << pyre::journal::newline
        << "  nudge: " << packing.nudge() << pyre::journal::newline
        << "  strides: " << packing.strides() << pyre::journal::endl(__HERE__);

    // sign on
    channel << "visiting:" << pyre::journal::newline;
    // visit every spot in column major order
    for (auto idx : packing.order(canonical_t::order_type::fortran())) {
        // show me
        channel << " at: " << idx << pyre::journal::newline;
    }
    // flush
    channel << pyre::journal::endl(__HERE__);


    // all done
    return 0;
}


// end of file
