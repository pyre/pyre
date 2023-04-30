// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the grid
#include <pyre/grid.h>


// type alias
using index_t = pyre::grid::index_t<4>;


// exercise the {zero} factory
int main(int argc, char * argv[]) {
    // make an index filled with zeroes
    constexpr index_t index = index_t::zero();

    // verify the contents
    static_assert (index[0] == 0);
    static_assert (index[1] == 0);
    static_assert (index[2] == 0);
    static_assert (index[3] == 0);

    // all done
    return 0;
}


// end of file
