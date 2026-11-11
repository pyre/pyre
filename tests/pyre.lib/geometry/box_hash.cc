// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that equal boxes hash alike, and that the order of the edges shapes the hash


// portability
#include <portinfo>
// STL
#include <cassert>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
using box_t = pyre::geometry::box_t<chart_t>;


// driver
int
main()
{
    // a box across the antimeridian
    auto box = box_t(170, -10, -170, 10);
    // hashes like another made the same way
    assert(box.hash() == box_t(170, -10, -170, 10).hash());
    // the box with its west and east edges swapped is the rest of the band
    auto rest = box_t(-170, -10, 170, 10);
    // which is a different box
    assert(box != rest);
    // with a different hash
    assert(box.hash() != rest.hash());
    // and the whole sphere hashes like itself
    assert(box_t::sphere().hash() == box_t::sphere().hash());

    // all done
    return 0;
}


// end of file
