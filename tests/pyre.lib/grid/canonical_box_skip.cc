// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using canonical_t = pyre::grid::canonical_t<2>;


// simple check that the map from index space to offsets is correct
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("canonical_box");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.canonical");

    // pick a shape
    canonical_t::shape_type shape { 32, 32 };
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
        << "    nudge: " << packing.nudge() << pyre::journal::newline
        << "    begin: " << *packing.begin() << pyre::journal::newline
        << "    end: " << *packing.end() << pyre::journal::endl(__HERE__);

    // pick a spot
    canonical_t::index_type spot { 2, 3 };
    // and a shape
    canonical_t::shape_type sliceShape { 16, 16 };
    // extract the region
    auto box = packing.box(spot, sliceShape);
    // show me
    channel
        << "box:" << pyre::journal::newline
        << "    base: " << spot << pyre::journal::newline
        << "    shape: " << box.shape() << pyre::journal::newline
        << "    origin: " << box.origin() << pyre::journal::newline
        << "    order: " << box.order() << pyre::journal::newline
        << "    strides: " << box.strides() << pyre::journal::newline
        << "    cells: " << box.cells() << pyre::journal::newline
        << "    nudge: " << box.nudge() << pyre::journal::newline
        << "    begin: " << *box.begin() << pyre::journal::newline
        << "    end: " << *box.end() << pyre::journal::endl(__HERE__);

    // verify that the iteration limits are as expected
    assert(( *box.begin() == spot ));
    assert(( *box.end() == spot + sliceShape ));

    // set up a skip
    canonical_t::index_type skip { 4, 2 };

    // visit it
    channel << "box:" << pyre::journal::newline;
    for (auto i = box.begin(skip); i != box.end(); ++i) {
        // dereference to get the index
        auto idx = *i;
        // show me
        channel
            << "  " << idx << " -> " << box[idx] << " == " << packing[idx]
            << pyre::journal::newline;
        // verify that the index resolves to the same spot in both layouts
        assert(( packing[idx] == box[idx] ));
    }
    // flush
    channel << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
