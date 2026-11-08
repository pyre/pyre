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


// bind the boxes of the longitude-latitude chart of the sphere
void
pyre::py::geometry::box(py::module & m)
{
    // wrap the box
    auto cls = py::class_<box_t>(
        // the scope
        m,
        // the name of the class
        "SphereBox",
        // its docstring
        "the points of the sphere between two meridians and two parallels");

    // the empty box
    cls.def(
        // the constructor
        py::init<>(),
        // the docstring
        "the empty box");
    // the box between two meridians and two parallels
    cls.def(
        // the constructor
        py::init<double, double, double, double>(),
        // the signature
        "west"_a, "south"_a, "east"_a, "north"_a,
        // the docstring
        "the points from the meridian at {west} east to the one at {east}, and from the parallel "
        "at {south} to the one at {north}, in degrees");
    // the whole sphere
    cls.def_static(
        // the name
        "sphere",
        // the implementation
        &box_t::sphere,
        // the docstring
        "the box that holds the whole sphere");

    // the west edge
    cls.def_property_readonly(
        // the name
        "west",
        // the implementation
        &box_t::west,
        // the docstring
        "the longitude of my west edge, in degrees");
    // the south edge
    cls.def_property_readonly(
        // the name
        "south",
        // the implementation
        &box_t::south,
        // the docstring
        "the latitude of my south edge, in degrees");
    // the east edge
    cls.def_property_readonly(
        // the name
        "east",
        // the implementation
        &box_t::east,
        // the docstring
        "the longitude of my east edge, in degrees");
    // the north edge
    cls.def_property_readonly(
        // the name
        "north",
        // the implementation
        &box_t::north,
        // the docstring
        "the latitude of my north edge, in degrees");
    // the degrees of longitude it spans
    cls.def_property_readonly(
        // the name
        "width",
        // the implementation
        &box_t::width,
        // the docstring
        "the degrees of longitude from my west edge east to my east edge");
    // whether it holds anything
    cls.def_property_readonly(
        // the name
        "empty",
        // the implementation
        &box_t::empty,
        // the docstring
        "whether i hold no points");
    // whether it holds every longitude
    cls.def_property_readonly(
        // the name
        "full",
        // the implementation
        &box_t::full,
        // the docstring
        "whether i hold every longitude");

    // whether it holds a point
    cls.def(
        // the name
        "contains",
        // the implementation
        &box_t::contains,
        // the signature
        "point"_a,
        // the docstring
        "check whether i hold {point}");
    // the box itself, as its envelope
    cls.def(
        // the name
        "envelope",
        // the implementation
        &box_t::envelope,
        // the docstring
        "the smallest box that holds me: myself");
    // the polygon with its points
    cls.def(
        // the name
        "polygon",
        // the implementation
        &box_t::polygon,
        // the docstring
        "the polygon with my points; i must not be empty");

    // the relations with the other shapes of the sphere
    relateMethods<box_t, place_t, box_t, path_t, polygon_t, polygons_t>(cls);

    // two boxes compare equal when they have the same edges
    cls.def(py::self == py::self);

    // a readable representation
    cls.def(
        // the name
        "__repr__",
        // the handler spells out the edges
        [](const box_t & self) {
            // make a buffer
            auto buffer = std::ostringstream {};
            // write the edges
            buffer << "SphereBox(west=" << self.west() << ", south=" << self.south()
                   << ", east=" << self.east() << ", north=" << self.north() << ")";
            // and hand off its contents
            return buffer.str();
        });

    // all done
    return;
}


// end of file
