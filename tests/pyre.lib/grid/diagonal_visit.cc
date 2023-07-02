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
using diagonal_t = pyre::grid::diagonal_t<3>;


// simple check that the map from index space to offsets is correct
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("diagonal_visit");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.diagonal");

    // pick a shape
    diagonal_t::shape_type shape { 3, 3, 3 };
    // pick an origin
    diagonal_t::index_type origin { -2, -2, -2 };
    // make a canonical packing strategy
    diagonal_t packing { shape, origin };
    // show me
    channel << "packing:" << pyre::journal::newline << "  shape: " << packing.shape()
            << pyre::journal::newline << "  order: " << packing.order() << pyre::journal::newline
            << "  origin: " << packing.origin() << pyre::journal::newline
            << "  nudge: " << packing.nudge() << pyre::journal::endl(__HERE__);

    // sign on
    channel << "visiting in packing order:" << pyre::journal::newline;
    // setup a counter
    int i = 0;
    // visit every spot
    for (auto idx : packing) {
        // get the offset of this index
        auto offset = packing[idx];
        // show me
        channel << " at: " << idx << " -> " << offset << pyre::journal::newline;
        channel << "\t -> " << (packing[offset])[0] << " " << (packing[offset])[1] << " "
                << (packing[offset])[2] << pyre::journal::newline;
        // if the index is diagonal
        if (idx[0] == idx[1] && idx[1] == idx[2]) {
            // verify that we are visiting in packing order
            assert((offset == i));
            // verify the inverse packing relation
            assert((idx == packing[offset]));
            // increment the counter and grab the next index
            ++i;
        }
    }
    // flush
    channel << pyre::journal::endl(__HERE__);


    // all done
    return 0;
}


// end of file
