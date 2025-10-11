// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using canonical_t = pyre::grid::canonical_t<2, long>;


// verify that the layout is recorded as requested
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("canonical_long");
    // make a channel
    auto channel = pyre::journal::debug_t("pyre.grid.canonical");

    // pick a shape
    canonical_t::shape_type shape { 2, 3 };
    // make a canonical packing strategy
    canonical_t packing { shape };

    // show me
    channel << "shape: " << packing.shape() << pyre::journal::newline
            << "origin: " << packing.origin() << pyre::journal::newline
            << "order: " << packing.order() << pyre::journal::newline
            << "strides: " << packing.strides() << pyre::journal::newline
            << "nudge: " << packing.nudge() << pyre::journal::endl(__HERE__);

    // verify we understand the default constructor
    assert((packing.shape() == shape));
    assert((packing.order() == canonical_t::order_type::c()));
    assert((packing.origin() == canonical_t::index_type::zero()));
    assert((packing.nudge() == packing[{ 0, 0 }]));

    // make an iterator
    auto idx = packing.begin();
    // show me
    channel << "begin: " << *idx << pyre::journal::endl;
    // increment
    ++idx;
    // show me
    channel << "begin: " << *idx << pyre::journal::endl;
    assert((*idx == canonical_t::index_type { 0, 1 }));

    // all done
    return 0;
}


// end of file
