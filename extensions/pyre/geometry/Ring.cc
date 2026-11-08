// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// bind the rings on the sphere; a ring bounds the region to its left, as one walks it from vertex
// to vertex seen from outside the sphere, so a ring walked the wrong way describes the complement
// of what was meant; see {pyre::geometry::Ring} and doc/design/geometry.md for why
void
pyre::py::geometry::ring(py::module & m)
{
    // wrap the ring
    auto cls = py::class_<ring_t>(
        // the scope
        m,
        // the name of the class
        "SphereRing",
        // its docstring
        "a closed sequence of points of the sphere, and the region to its left");

    // the ring through a sequence of points
    cls.def(
        // the constructor
        py::init<const ring_t::vertices_type &, bool>(),
        // the signature
        "vertices"_a, "geodesic"_a = true,
        // the docstring
        "the ring through {vertices}, which bounds the region to its left, with edges that are "
        "great-circle arcs when {geodesic} is true, and straight in the longitude-latitude chart "
        "otherwise; the ring closes itself");

    // the vertices
    cls.def_property_readonly(
        // the name
        "vertices",
        // the implementation
        &ring_t::vertices,
        // the docstring
        "my vertices");
    // the kind of edges
    cls.def_property_readonly(
        // the name
        "geodesic",
        // the implementation
        &ring_t::geodesic,
        // the docstring
        "whether my edges are great-circle arcs");
    // the area of the region it bounds
    cls.def_property_readonly(
        // the name
        "area",
        // the implementation
        &ring_t::area,
        // the docstring
        "the area of the region to my left, in steradians on the unit sphere");

    // whether a point is in the region
    cls.def(
        // the name
        "contains",
        // the implementation
        &ring_t::contains,
        // the signature
        "point"_a,
        // the docstring
        "check whether {point} is in the region to my left, which includes me");
    // whether a point is on the ring
    cls.def(
        // the name
        "boundary",
        // the implementation
        &ring_t::boundary,
        // the signature
        "point"_a,
        // the docstring
        "check whether {point} is on me");
    // the ring walked the other way
    cls.def(
        // the name
        "reversed",
        // the implementation
        &ring_t::reversed,
        // the docstring
        "the ring through my vertices in the opposite order, which bounds the other region");
    // the box around the region
    cls.def(
        // the name
        "envelope",
        // the implementation
        &ring_t::envelope,
        // the docstring
        "the smallest box that holds the region to my left");

    // two rings compare equal when they have the same vertices, in the same order, and the same
    // kind of edges
    cls.def(py::self == py::self);

    // all done
    return;
}


// end of file
