// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/_grid_.h>


// the shape under test
using shape_t = pyre::grid::shape_t<4>;


// exercise the {zero} factory
int
main()
{
    // ask for a shape with no extent on any axis
    constexpr shape_t shape = shape_t::zero();

    // the first axis is degenerate
    static_assert(shape[0] == 0);
    // and so is every other one
    static_assert(shape[1] == 0);
    static_assert(shape[2] == 0);
    static_assert(shape[3] == 0);

    // a shape that is degenerate anywhere addresses nothing at all
    static_assert(shape.cells() == 0);

    // all done
    return 0;
}


// end of file
