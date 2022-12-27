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
using shp1_t = pyre::grid::shape_t<1>;
using shp3_t = pyre::grid::shape_t<3>;
using shp4_t = pyre::grid::shape_t<4>;


// exercise the cartesian product of two indices
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("shape_cartesian");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // make a 1d shape
    constexpr shp1_t shp_1 { 1 };
    // make a 3d shape
    constexpr shp3_t shp_3 { 1, 1, 1 };
    // combine
    auto shift = shp_1 * shp_3;

    // make an explicit one
    shp4_t sample { 1, 2, 3, 4 };
    // derive one
    auto actual = sample + shift;
    // the expected result
    shp4_t expected { 2, 3, 4, 5 };

    // show me
    channel
        << "   shp_1: { " << shp_1 << " }" << pyre::journal::newline
        << "   shp_3: { " << shp_3 << " }" << pyre::journal::newline
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
