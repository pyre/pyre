// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// package declarations
#include "__init__.h"


// build the submodule
void
pyre::py::geometry::__init__(py::module & m)
{
    // create a {geometry} submodule
    auto geometry = m.def_submodule(
        // the name of the module
        "geometry",
        // its docstring
        "wrappers over {pyre::geometry}: spaces, their points, and the shapes in them");

    // register every class before binding any interface, since the signatures name the
    // classes they traffic in, and the shapes refer to each other: the points
    pointClasses(geometry);
    // the shapes of the lines
    intervalClasses(geometry);
    // the shapes of the sphere
    boxClass(geometry);
    pathClass(geometry);
    ringClass(geometry);
    polygonClass(geometry);
    // the unions of both
    collectionClasses(geometry);
    // the spaces
    timelineClass(geometry);
    // and the charts
    lonlatClass(geometry);

    // now bind their interfaces: the points
    point();
    // the shapes of the lines
    interval();
    // the shapes of the sphere
    box();
    path();
    ring();
    polygon();
    // the unions of both
    collection();
    // the spaces
    timeline();
    // the charts
    lonlat();
    // the relations
    relations(geometry);
    // and the constructions
    constructions(geometry);

    // all done
    return;
}


// end of file
