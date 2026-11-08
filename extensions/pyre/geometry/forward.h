// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {geometry} binding namespace
namespace pyre::py::geometry {
    // the timeline
    using timeline_t = pyre::geometry::timeline_t;
    // its points
    using instant_t = pyre::geometry::point_t<timeline_t>;
    // its intervals
    using interval_t = pyre::geometry::interval_t<timeline_t>;
    // and their unions
    using intervals_t = pyre::geometry::collection_t<interval_t>;

    // the sphere
    using sphere_t = pyre::geometry::sphere_t;
    // its points
    using place_t = pyre::geometry::point_t<sphere_t>;
    // the longitude-latitude chart on it
    using lonlat_t = pyre::geometry::lonlat_t<sphere_t>;
    // and the shapes in that chart
    using box_t = pyre::geometry::box_t<lonlat_t>;
    using path_t = pyre::geometry::path_t<lonlat_t>;
    using ring_t = pyre::geometry::ring_t<lonlat_t>;
    using polygon_t = pyre::geometry::polygon_t<lonlat_t>;
    // the unions of polygons
    using polygons_t = pyre::geometry::collection_t<polygon_t>;

    // bind the points
    void point(py::module &);
    // bind the intervals
    void interval(py::module &);
    // bind the boxes
    void box(py::module &);
    // bind the paths
    void path(py::module &);
    // bind the rings
    void ring(py::module &);
    // bind the polygons
    void polygon(py::module &);
    // bind the unions
    void collection(py::module &);
    // bind the spaces
    void timeline(py::module &);
    // bind the charts
    void lonlat(py::module &);
    // bind the relations among shapes
    void relations(py::module &);
    // bind the shapes built out of other shapes
    void constructions(py::module &);
} // namespace pyre::py::geometry


// end of file
