// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using index_t = pyre::grid::index_t<2>;


// index scaling
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_scaling");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // an index
    constexpr index_t ref { 128, 128 };
    // a margin
    constexpr index_t margin { 32, 32 };
    // use it to make another one
    constexpr index_t sec = ref + 2*margin;

    // make an index out a combination of these
    index_t cor = sec - ref + index_t::one();

    // show me
    channel
        << "ref: " << ref << pyre::journal::newline
        << "sec: " << sec << pyre::journal::newline
        << "cor: " << cor << pyre::journal::endl(__HERE__);

    // verify
    for (auto axis = 0; axis < index_t::rank(); ++axis) {
        assert(( cor[axis] == sec[axis] - ref[axis] + 1 ));
    }

    // all done
    return 0;
}


// end of file
