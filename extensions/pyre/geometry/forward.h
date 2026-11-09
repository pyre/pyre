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

    // register the classes of the points
    void pointClasses(py::module &);
    // of the intervals
    void intervalClasses(py::module &);
    // of the boxes
    void boxClass(py::module &);
    // of the paths
    void pathClass(py::module &);
    // of the rings
    void ringClass(py::module &);
    // of the polygons
    void polygonClass(py::module &);
    // of the unions
    void collectionClasses(py::module &);
    // of the spaces
    void timelineClass(py::module &);
    // and of the charts
    void lonlatClass(py::module &);

    // bind the points
    void point();
    // bind the intervals
    void interval();
    // bind the boxes
    void box();
    // bind the paths
    void path();
    // bind the rings
    void ring();
    // bind the polygons
    void polygon();
    // bind the unions
    void collection();
    // bind the spaces
    void timeline();
    // bind the charts
    void lonlat();
    // bind the relations among shapes
    void relations(py::module &);
    // bind the shapes built out of other shapes
    void constructions(py::module &);
} // namespace pyre::py::geometry


// end of file
