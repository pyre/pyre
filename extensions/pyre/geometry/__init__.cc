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

    // bind the shapes first, since the spaces, the charts, the relations and the constructions
    // traffic in them: the points come first, since they are the ends and the vertices of the
    // others
    point(geometry);
    // then the shapes of the lines
    interval(geometry);
    // the shapes of the sphere, the rings before the polygons they bound
    box(geometry);
    path(geometry);
    ring(geometry);
    polygon(geometry);
    // and the unions of both
    collection(geometry);
    // the spaces
    timeline(geometry);
    // the charts
    lonlat(geometry);
    // the relations
    relations(geometry);
    // and the constructions
    constructions(geometry);

    // all done
    return;
}


// end of file
