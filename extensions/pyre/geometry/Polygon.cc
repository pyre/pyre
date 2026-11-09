// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// the bindings of the relations
#include "relations.h"


// register the class of the polygons, so that every signature can name it
void
pyre::py::geometry::polygonClass(py::module & m)
{
    // register the polygon
    py::class_<polygon_t>(
        // the scope
        m,
        // the name of the class
        "SpherePolygon",
        // its docstring
        "the points of the sphere in the regions bound by all of its rings");

    // all done
    return;
}


// bind the polygons on the sphere: the regions bound by all of their rings
void
pyre::py::geometry::polygon()
{
    // the class of the polygon, registered by {polygonClass}
    auto cls = py::class_<polygon_t>(py::type::of<polygon_t>());

    // the polygon bound by a sequence of rings
    cls.def(
        // the constructor
        py::init<const polygon_t::rings_type &>(),
        // the signature
        "rings"_a,
        // the docstring
        "the points in the regions bound by all of the {rings}: the first one counterclockwise "
        "around the polygon, the others clockwise around its holes; no rings is the whole sphere");

    // the rings
    cls.def_property_readonly(
        // the name
        "rings",
        // the implementation
        &polygon_t::rings,
        // the docstring
        "my rings");

    // whether a point is in it
    cls.def(
        // the name
        "contains",
        // the implementation
        &polygon_t::contains,
        // the signature
        "point"_a,
        // the docstring
        "check whether {point} is in me, boundary included");
    // the box around it
    cls.def(
        // the name
        "envelope",
        // the implementation
        &polygon_t::envelope,
        // the docstring
        "the smallest box that holds me");

    // the relations with the other shapes of the sphere
    relateMethods<polygon_t, place_t, box_t, path_t, polygon_t, polygons_t>(cls);

    // two polygons compare equal when they have the same rings
    cls.def(py::self == py::self);

    // all done
    return;
}


// end of file
