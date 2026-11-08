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


// bind the relations
void
pyre::py::geometry::relations(py::module & m)
{
    // between intervals of the timeline
    relate<interval_t, interval_t>(m);
    // between intervals and their unions, in either order
    relate<interval_t, intervals_t>(m);
    relate<intervals_t, interval_t>(m);
    // and between unions
    relate<intervals_t, intervals_t>(m);

    // between the shapes of the sphere, in every order the library has
    relateAll<place_t, box_t, path_t, polygon_t, polygons_t>(m);

    // all done
    return;
}


// end of file
