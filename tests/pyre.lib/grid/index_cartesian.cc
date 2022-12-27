// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
#include <typeinfo>
// get the grid
#include <pyre/grid.h>


// type alias
using idx1_t = pyre::grid::index_t<1>;
using idx3_t = pyre::grid::index_t<3>;
using idx4_t = pyre::grid::index_t<4>;


// exercise the cartesian product of two indices
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_cartesian");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // make a 1d index
    constexpr idx1_t idx_1 { 1 };
    // make a 3d index
    constexpr idx3_t idx_3 { 1, 1, 1 };
    // combine
    auto shift = idx_1 * idx_3;

    // make an explicit one
    idx4_t sample { 1, 2, 3, 4 };
    // derive one
    auto actual = sample + shift;
    // the expected result
    idx4_t expected { 2, 3, 4, 5 };

    // show me
    channel
        << "   idx_1: { " << idx_1 << " }" << pyre::journal::newline
        << "   idx_3: { " << idx_3 << " }" << pyre::journal::newline
        << "   shift: { " << shift << " }" << pyre::journal::newline
        << "  sample: { " << sample << " }" << pyre::journal::newline
        << "  actual: { " << actual << " }" << pyre::journal::newline
        << "expected: { " << actual << " }" << pyre::journal::newline
        << pyre::journal::endl(__HERE__);

    // check
    assert(( actual == expected ));

    // all done
    return 0;
}


// end of file
