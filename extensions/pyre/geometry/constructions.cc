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

    // all done
    return;
}


// end of file
