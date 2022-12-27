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


// exercise the {zero} factory
int
main(int argc, char * argv[])
{
    // make an shape filled with zeroes
    constexpr shape_t shape = shape_t::zero();

    // verify the contents
    static_assert(shape[0] == 0);
    static_assert(shape[1] == 0);
    static_assert(shape[2] == 0);
    static_assert(shape[3] == 0);

    // and that the interface is still accessible
    assert(shape.cells() == 0);

    // all done
    return 0;
}


// end of file
