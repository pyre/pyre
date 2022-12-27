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


// exercise the filling constructor
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_fill");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // pick a value
    constexpr idx_t::rank_type u = 42;
    // make a const index
    constexpr idx_t idx_1 { u };
    // show me
    channel
        << "idx_1: " << idx_1
        << pyre::journal::endl(__HERE__);
    // verify the contents
    static_assert (idx_1[0] == u);
    static_assert (idx_1[1] == u);
    static_assert (idx_1[2] == u);
    static_assert (idx_1[3] == u);

    // again, at runtime
    idx_t::rank_type v = argc;
    // with another index
    const idx_t idx_2 { v };
    // show me
    channel
        << "idx_2: " << idx_2
        << pyre::journal::endl(__HERE__);
    // verify the contents
    assert(( idx_2[0] == v ));
    assert(( idx_2[1] == v ));
    assert(( idx_2[2] == v ));
    assert(( idx_2[3] == v ));

    // all done
    return 0;
}


// end of file
