// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using symmetric_t = pyre::grid::symmetric_t<5>;


// simple check that the map from index space to offsets is correct
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("symmetric_visit");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.symmetric");

    // pick a shape
    symmetric_t::shape_type shape { 4, 4, 4, 4, 4 };
    // make a canonical packing strategy
    symmetric_t packing { shape };
    // show me
    channel << "packing:" << pyre::journal::newline << "  shape: " << packing.shape()
            << pyre::journal::newline << "  order: " << packing.order() << pyre::journal::newline
            << "  origin: " << packing.origin() << pyre::journal::endl(__HERE__);

    // sign on
    channel << "visiting in packing order:" << pyre::journal::newline;
    // visit every spot
    for (auto idx : packing) {
        // get the offset of this index
        auto offset = packing[idx];
        // show me
        channel << " at: " << idx << " -> " << offset << pyre::journal::newline;
        // sort the indices
        std::sort(idx.begin(), idx.end());
        // verify that we are visiting in packing order
        assert((idx == packing[offset]));
    }
    // flush
    channel << pyre::journal::endl(__HERE__);


    // all done
    return 0;
}


// end of file
