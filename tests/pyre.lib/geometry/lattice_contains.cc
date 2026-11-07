// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that a lattice counts its points and recognizes them, corners included


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using space_t = pyre::geometry::lattice_t<2>;
using point_t = pyre::geometry::point_t<space_t>;


// driver
int
main()
{
    // the tracks and frames of a catalog
    auto catalog = space_t({ 1, 1 }, { 173, 176 });

    // the lattice has a point for every pair
    assert(catalog.cells() == 173 * 176);
    // its corners belong to it
    assert(catalog.contains(point_t(1L, 1L)));
    assert(catalog.contains(point_t(173L, 176L)));
    // and so do the points between them
    assert(catalog.contains(point_t(77L, 69L)));
    // but not the points past its edges
    assert(not catalog.contains(point_t(0L, 69L)));
    assert(not catalog.contains(point_t(77L, 177L)));

    // a lattice whose corners are in the wrong order is empty
    auto empty = space_t({ 2, 1 }, { 1, 1 });
    assert(empty.cells() == 0);

    // all done
    return 0;
}


// end of file
