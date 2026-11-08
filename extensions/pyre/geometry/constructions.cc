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
    // bind the constructions on the intervals of a line
    template <class lineT>
    inline void lineConstructions(py::module & m)
    {
        // the interval
        using interval_t = pyre::geometry::interval_t<lineT>;
        // and its unions
        using union_t = pyre::geometry::collection_t<interval_t>;

        // the hull of two intervals
        m.def(
            // the name
            "hull",
            // the implementation
            [](const interval_t & a, const interval_t & b) {
                // ask the construction
                return pyre::geometry::hull(a, b);
            },
            // the signature
            "a"_a, "b"_a,
            // the docstring
            "the smallest interval that holds both {a} and {b}");

        // the union of intervals
        m.def(
            // the name
            "union",
            // the implementation
            [](const std::vector<interval_t> & shapes) {
                // collect them
                return union_t(shapes);
            },
            // the signature
            "shapes"_a,
            // the docstring
            "the union of the intervals in {shapes}");

        // all done
        return;
    }
} // namespace pyre::py::geometry


// bind the constructions
void
pyre::py::geometry::constructions(py::module & m)
{
    // on the intervals of the timeline
    lineConstructions<timeline_t>(m);

    // on the shapes of the sphere: the hull of two boxes
    m.def(
        // the name
        "hull",
        // the implementation
        [](const box_t & a, const box_t & b) {
            // ask the construction
            return pyre::geometry::hull(a, b);
        },
        // the signature
        "a"_a, "b"_a,
        // the docstring
        "the smallest box that holds both {a} and {b}, the shorter way around in longitude");
    // the union of polygons
    m.def(
        // the name
        "union",
        // the implementation
        [](const std::vector<polygon_t> & shapes) {
            // collect them
            return polygons_t(shapes);
        },
        // the signature
        "shapes"_a,
        // the docstring
        "the union of the polygons in {shapes}");
    // a ring walked so that it bounds the smaller of its two regions; this is the right reading
    // of rings drawn or typed by people, which come in either direction, and the wrong one for
    // data whose convention is known; see {pyre::geometry::orient}
    m.def(
        // the name
        "orient",
        // the implementation
        [](const ring_t & ring) {
            // ask the construction
            return pyre::geometry::orient(ring);
        },
        // the signature
        "shape"_a,
        // the docstring
        "the ring {shape}, walked so that it bounds the smaller of its two regions");
    // and a polygon whose first ring bounds the smaller region and whose holes the larger
    m.def(
        // the name
        "orient",
        // the implementation
        [](const polygon_t & polygon) {
            // ask the construction
            return pyre::geometry::orient(polygon);
        },
        // the signature
        "shape"_a,
        // the docstring
        "the polygon {shape}, with its first ring around the smaller of its two regions and its "
        "holes around the larger");

    // all done
    return;
}


// end of file
