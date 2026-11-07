// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// check the boxes of the longitude-latitude chart: the points they hold, including the boxes that
// straddle the antimeridian and the ones that go all the way around; the empty box; and the hull
// of two boxes, the shorter way around


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
    // the chart
    auto chart = chart_t();
    // the point at a longitude and a latitude
    auto at = [&chart](double longitude, double latitude) {
        // place it
        return chart.point({ longitude, latitude });
    };

    // a box around the mediterranean
    auto sea = box_t(-6, 30, 36, 46);
    // holds the points inside
    assert(sea.contains(at(15, 38)));
    // and on its edges
    assert(sea.contains(at(-6, 30)));
    // but nothing outside
    assert(not sea.contains(at(40, 38)));
    assert(not sea.contains(at(15, 50)));

    // a box across the antimeridian, from 170 degrees east to 170 degrees west
    auto pacific = box_t(170, -10, -170, 10);
    // is twenty degrees wide
    assert(pacific.width() == 20);
    // holds the points on either side of the antimeridian
    assert(pacific.contains(at(175, 0)));
    assert(pacific.contains(at(-175, 0)));
    // and on it
    assert(pacific.contains(at(180, 0)));
    // but not the points on the other side of the earth
    assert(not pacific.contains(at(0, 0)));

    // a box that goes all the way around
    auto band = box_t(-180, 60, 180, 90);
    // holds every longitude
    assert(band.full());
    // up to the pole
    assert(band.contains(at(123, 89.9)));
    // and so does one given with any other start
    assert(box_t(10, 60, 370, 90) == band);

    // a box with its parallels out of order
    auto backwards = box_t(0, 10, 10, -10);
    // is the empty one
    assert(backwards.empty());
    assert(backwards == box_t());
    // and holds nothing
    assert(not backwards.contains(at(5, 0)));

    // the hull of two boxes on either side of the antimeridian
    auto hull = pyre::geometry::hull(box_t(170, 0, 175, 5), box_t(-175, -5, -170, 0));
    // goes the shorter way around, across the antimeridian
    assert(hull == box_t(170, -5, -170, 5));
    // and the hull with the empty box adds nothing
    assert(pyre::geometry::hull(sea, box_t()) == sea);

    // all done
    return 0;
}


// end of file
