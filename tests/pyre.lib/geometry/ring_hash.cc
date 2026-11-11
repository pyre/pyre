// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that equal rings hash alike, and that a ring and its reverse, which bound complementary
// regions, hash differently


// portability
#include <portinfo>
// STL
#include <cassert>
#include <vector>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
using ring_t = pyre::geometry::ring_t<chart_t>;


// driver
int
main()
{
    // the chart
    auto chart = chart_t();
    // the point at a longitude and a latitude
    auto at = [&chart](double longitude, double latitude) {
        // place it
        return chart.point({ longitude, latitude });
    };
    // the corners of a small square, walked counterclockwise
    auto corners = std::vector { at(0, 0), at(10, 0), at(10, 10), at(0, 10) };

    // a ring through them
    auto ring = ring_t(corners);
    // hashes like another made the same way
    assert(ring.hash() == ring_t(corners).hash());
    // the ring walked the other way
    auto reversed = ring.reversed();
    // is a different ring
    assert(ring != reversed);
    // with a different hash
    assert(ring.hash() != reversed.hash());

    // all done
    return 0;
}


// end of file
