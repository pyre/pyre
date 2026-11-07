// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that longitude and latitude map to unit normals and back, across the globe and on both
// sides of the antimeridian


// portability
#include <portinfo>
// STL
#include <cassert>
#include <cmath>
// support
#include <pyre/geometry.h>


// type aliases
using space_t = pyre::geometry::ellipsoid_t;
using chart_t = pyre::geometry::lonlat_t<space_t>;


// driver
int
main()
{
    // the chart
    auto chart = chart_t();

    // go through a grid of longitudes and latitudes, short of the poles, where the longitude is
    // not defined
    for (auto lon = -179.5; lon < 180; lon += 7.25) {
        for (auto lat = -89.5; lat < 90; lat += 3.5) {
            // make the point
            auto p = chart.point({ lon, lat });
            // its normal has unit length
            const auto & n = p.data();
            assert(std::abs(n[0] * n[0] + n[1] * n[1] + n[2] * n[2] - 1) < 1e-15);
            // and the chart recovers the coordinates
            auto [lambda, phi] = chart.coordinates(p);
            assert(std::abs(lambda - lon) < 1e-12);
            assert(std::abs(phi - lat) < 1e-12);
        }
    }

    // the north pole is the normal along the axis
    auto pole = chart.point({ 0.0, 90.0 });
    assert(std::abs(pole[2] - 1) < 1e-15);

    // all done
    return 0;
}


// end of file
