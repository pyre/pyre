// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using canonical_t = pyre::grid::canonical_t<3>;


// verify that the nudge gets computed correctly
int main() {
    // pick a shape
    canonical_t::shape_type shape { 2,3,4 };
    // pick the index origin
    canonical_t::index_type origin { -1, -1, -1 };
    // make a canonical packing strategy
    canonical_t packing { shape, origin };

    // check the nudge against an explicit calculation
    assert(( packing.nudge() == 17 ));
    // verify it is the offset of the zero index
    assert(( packing.nudge() == packing[{0,0,0}] ));

    // all done
    return 0;
}


// end of file
