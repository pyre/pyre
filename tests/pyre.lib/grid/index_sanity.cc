// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using index_t = pyre::grid::index_t<4>;


// sanity check
int main(int argc, char *argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_sanity");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // make a default index
    constexpr index_t dflt {};
    // show me
    channel
        << "default: " << dflt
        << pyre::journal::endl(__HERE__);
    // verify that the index dimensionality is reported correctly through the type
    static_assert (index_t::rank() == 4);
    // verify that the index dimensionality is reported correctly through an instance
    static_assert (dflt.rank() == 4);

    // make an explicitly initialized index
    constexpr index_t idx { 0,1,2,3 };
    // show me
    channel
        << "idx: " << idx
        << pyre::journal::endl(__HERE__);

    // make a zero index using the static factory
    constexpr index_t z = index_t::zero();
    // show me
    channel
        << "zero: " << z
        << pyre::journal::endl(__HERE__);
    // verify it's the same as {dflt}
    assert(( z == dflt ));

    // make an index using the filling constructor
    index_t zero(0);
    // show me
    channel
        << "another zero: " << zero
        << pyre::journal::endl(__HERE__);
    // verify it's the same as {z}
    assert(( zero == z ));

    // all done
    return 0;
}


// end of file
