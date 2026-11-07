// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// helpers
namespace pyre::py::geometry {
    // bind the relations between a pair of kinds of shapes
    template <class firstT, class secondT>
    inline void relate(py::module & m)
    {
        // whether the two share a point
        m.def(
            // the name
            "intersects",
            // the implementation
            [](const firstT & a, const secondT & b) {
                // ask the relation
                return pyre::geometry::intersects(a, b);
            },
            // the signature
            "a"_a, "b"_a,
            // the docstring
            "check whether {a} and {b} share a point");
        // whether the first covers the second
        m.def(
            // the name
            "covers",
            // the implementation
            [](const firstT & a, const secondT & b) {
                // ask the relation
                return pyre::geometry::covers(a, b);
            },
            // the signature
            "a"_a, "b"_a,
            // the docstring
            "check whether every point of {b} is a point of {a}");

        // all done
        return;
    }
} // namespace pyre::py::geometry


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

    // all done
    return;
}


// end of file
