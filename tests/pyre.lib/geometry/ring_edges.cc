// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check that the edges of a ring are interpreted as asked: a geodesic edge between two points at
// the same latitude bulges toward the pole, while an edge straight in the chart follows the
// parallel, so a point just north of the parallel is inside one ring and outside the other


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

    // the corners of a ring whose north edge runs between two points at 60 degrees north
    auto corners = std::vector { at(0, 50), at(60, 50), at(60, 60), at(0, 60) };
    // with geodesic edges
    auto geodesic = ring_t(corners, true);
    // and with edges straight in the chart
    auto straight = ring_t(corners, false);
    // a point north of the parallel, under the bulge of the great circle
    auto point = at(30, 62);
    // is inside the ring with geodesic edges
    assert(geodesic.contains(point));
    // and outside the one with edges straight in the chart
    assert(not straight.contains(point));
    // while a point south of the parallel is inside both
    assert(geodesic.contains(at(30, 58)));
    assert(straight.contains(at(30, 58)));

    // all done
    return 0;
}


// end of file
