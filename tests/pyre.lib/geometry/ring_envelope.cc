// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the envelopes of rings: the box around the region a ring bounds, which straddles the
// antimeridian when the region does, reaches past the vertices where a geodesic edge bulges
// toward a pole, and holds every longitude up to a pole the region holds


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
// support
#include <pyre/geometry.h>


// type aliases
using chart_t = pyre::geometry::lonlat_t<pyre::geometry::sphere_t>;
using box_t = pyre::geometry::box_t<chart_t>;
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

    // a square across the antimeridian, with edges straight in the chart
    auto pacific = ring_t({ at(175, -5), at(-175, -5), at(-175, 5), at(175, 5) }, false);
    // has an envelope that straddles the antimeridian
    auto envelope = pacific.envelope();
    // from 175 degrees east
    assert(std::abs(envelope.west() - 175) < 1e-9);
    // to 175 degrees west
    assert(std::abs(envelope.east() + 175) < 1e-9);
    // and ten degrees wide
    assert(std::abs(envelope.width() - 10) < 1e-9);

    // a ring with a geodesic edge between two points at 60 degrees north
    auto bulge = ring_t({ at(0, 50), at(90, 50), at(90, 60), at(0, 60) });
    // reaches north of its vertices, where the edge bulges toward the pole
    assert(bulge.envelope().north() > 65);

    // a ring around the north pole
    auto cap = ring_t({ at(0, 80), at(90, 80), at(180, 80), at(270, 80) });
    // has an envelope that holds every longitude
    assert(cap.envelope().full());
    // up to the pole
    assert(cap.envelope().north() == 90);

    // all done
    return 0;
}


// end of file
