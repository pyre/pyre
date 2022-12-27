// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// type alias
using shape_t = pyre::grid::shape_t<4>;


// exercise operator[]
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("shape_access");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.shape");

    // make a const shape
    constexpr shape_t shape_1 { 0,1,2,3 };
    // show me
    channel
        << "shape_1: " << shape_1
        << pyre::journal::endl(__HERE__);
    // verify the contents
    static_assert (shape_1[0] == 0);
    static_assert (shape_1[1] == 1);
    static_assert (shape_1[2] == 2);
    static_assert (shape_1[3] == 3);

    // make a writable one
    shape_t shape_2 {};
    // show me
    channel
        << "shape_2 before: " << shape_2
        << pyre::journal::endl(__HERE__);
    // set it
    shape_2[0] = 0;
    shape_2[1] = 1;
    shape_2[2] = 2;
    shape_2[3] = 3;
    // show me
    channel
        << "shape_2 after: " << shape_2
        << pyre::journal::endl(__HERE__);

    // check it
    assert(( shape_2[0] == 0 ));
    assert(( shape_2[1] == 1 ));
    assert(( shape_2[2] == 2 ));
    assert(( shape_2[3] == 3 ));

    // all done
    return 0;
}


// end of file
