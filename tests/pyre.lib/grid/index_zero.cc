// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the index under test
using index_t = pyre::grid::index_t<4>;


// exercise the {zero} and {one} factories
int
main()
{
    // an index at the origin has every coordinate zeroed out
    constexpr index_t z = index_t::zero();
    // verify the first coordinate
    static_assert(z[0] == 0);
    // and the rest
    static_assert(z[1] == 0);
    static_assert(z[2] == 0);
    static_assert(z[3] == 0);

    // the unit index has every coordinate set to one
    constexpr index_t u = index_t::one();
    // verify the first
    static_assert(u[0] == 1);
    // and the rest
    static_assert(u[1] == 1);
    static_assert(u[2] == 1);
    static_assert(u[3] == 1);

    // all done
    return 0;
}


// end of file
