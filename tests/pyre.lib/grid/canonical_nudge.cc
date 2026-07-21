// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// the packing strategy under test
using canonical_t = pyre::grid::canonical_t<3>;


// verify that the nudge places an origin away from zero at the start of the block
int
main()
{
    // pick a shape
    constexpr canonical_t::shape_type shape { 2, 3, 4 };
    // and an origin that sits below zero on every axis
    constexpr canonical_t::index_type origin { -1, -1, -1 };
    // lay it out canonically
    constexpr canonical_t packing { shape, origin };

    // the nudge is the offset correction that pulls the origin back to zero; for this layout it
    // works out to seventeen
    static_assert(packing.nudge() == 17);

    // so the origin itself lands at the very start of the block
    static_assert(packing.offset(origin) == 0);
    // and the nudge equals the offset of the zero index, one step in along every axis
    static_assert(packing.nudge() == packing.offset({ 0, 0, 0 }));

    // all done
    return 0;
}


// end of file
