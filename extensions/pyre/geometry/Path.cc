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


// register the class of the paths, so that every signature can name it
void
pyre::py::geometry::pathClass(py::module & m)
{
    // register the path
    py::class_<path_t>(
        // the scope
        m,
        // the name of the class
        "SpherePath",
        // its docstring
        "a sequence of points of the sphere joined by edges");

    // all done
    return;
}


// bind the paths on the sphere
void
pyre::py::geometry::path()
{
    // the class of the path, registered by {pathClass}
    auto cls = py::class_<path_t>(py::type::of<path_t>());

    // the path through a sequence of points
    cls.def(
        // the constructor
        py::init<const path_t::vertices_type &, bool>(),
        // the signature
        "vertices"_a, "geodesic"_a = true,
        // the docstring
        "the path through {vertices}, with edges that are great-circle arcs when {geodesic} is "
        "true, and straight in the longitude-latitude chart otherwise");

    // the vertices
    cls.def_property_readonly(
        // the name
        "vertices",
        // the implementation
        &path_t::vertices,
        // the docstring
        "my vertices");
    // the kind of edges
    cls.def_property_readonly(
        // the name
        "geodesic",
        // the implementation
        &path_t::geodesic,
        // the docstring
        "whether my edges are great-circle arcs");

    // whether a point is on it
    cls.def(
        // the name
        "contains",
        // the implementation
        &path_t::contains,
        // the signature
        "point"_a,
        // the docstring
        "check whether {point} is on me");
    // the box around it
    cls.def(
        // the name
        "envelope",
        // the implementation
        &path_t::envelope,
        // the docstring
        "the smallest box that holds me");

    // the relations with the other shapes of the sphere
    relateMethods<path_t, place_t, box_t, path_t, polygon_t, polygons_t>(cls);

    // two paths compare equal when they have the same vertices and the same kind of edges
    cls.def(py::self == py::self);
    // and equal paths hash alike, so they can be members of sets and keys of dicts
    cls.def(
        // the name
        "__hash__",
        // the implementation
        &path_t::hash,
        // the docstring
        "my hash, shared by the paths that compare equal");

    // all done
    return;
}


// end of file
