// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// bind the longitude-latitude chart of the sphere, which names its points by their longitude
// and latitude, in degrees, longitude first
void
pyre::py::geometry::lonlat(py::module & m)
{
    // wrap the chart
    auto cls = py::class_<lonlat_t>(
        // the scope
        m,
        // the name of the class
        "SphereLonLat",
        // its docstring
        "the longitude-latitude chart of the sphere, in degrees");

    // build the chart
    cls.def(
        // the constructor
        py::init<>(),
        // the docstring
        "the longitude-latitude chart of the sphere");

    // the point at a longitude and a latitude
    cls.def(
        // the name
        "point",
        // the implementation
        [](const lonlat_t & self, double longitude, double latitude) {
            // ask the chart
            return self.point({ longitude, latitude });
        },
        // the signature
        "longitude"_a, "latitude"_a,
        // the docstring
        "the point at {longitude} and {latitude}, in degrees");

    // the longitude and latitude of a point
    cls.def(
        // the name
        "coordinates",
        // the implementation
        [](const lonlat_t & self, const place_t & point) {
            // ask the chart
            auto coordinates = self.coordinates(point);
            // and hand off the pair, longitude first
            return py::make_tuple(coordinates[0], coordinates[1]);
        },
        // the signature
        "point"_a,
        // the docstring
        "the longitude and latitude of {point}, in degrees, in that order");

    // all done
    return;
}


// end of file
