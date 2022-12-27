// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using idx_t = pyre::grid::index_t<4>;


// exercise operator[]
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_access");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // make a compile-time index
    constexpr idx_t idx_1 { 0,1,2,3 };
    // show me
    channel
        << "idx_1: " << idx_1
        << pyre::journal::endl(__HERE__);
    // verify the contents
    static_assert (idx_1[0] == 0);
    static_assert (idx_1[1] == 1);
    static_assert (idx_1[2] == 2);
    static_assert (idx_1[3] == 3);

    // make a writable one
    idx_t idx_2 { 0,0,0,0 };
    // show me
    channel
        << "idx_2 before: " << idx_2
        << pyre::journal::endl(__HERE__);
    // set it
    idx_2[0] = 0;
    idx_2[1] = 1;
    idx_2[2] = 2;
    idx_2[3] = 3;
    // show me
    channel
        << "idx_2 after: " << idx_2
        << pyre::journal::endl(__HERE__);
    // check it
    assert(( idx_2[0] == 0 ));
    assert(( idx_2[1] == 1 ));
    assert(( idx_2[2] == 2 ));
    assert(( idx_2[3] == 3 ));

    // all done
    return 0;
}


// end of file
