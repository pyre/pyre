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
    // bind the closed intervals of a line
    template <class lineT>
    inline void lineInterval(py::module & m, classname_t name, docstring_t docstring)
    {
        // the ends
        using point_t = pyre::geometry::point_t<lineT>;
        // the interval
        using interval_t = pyre::geometry::interval_t<lineT>;
        // and the unions of intervals
        using union_t = pyre::geometry::collection_t<interval_t>;

        // wrap the interval
        auto cls = py::class_<interval_t>(
            // the scope
            m,
            // the name of the class
            name,
            // its docstring
            docstring);

        // the empty interval
        cls.def(
            // the constructor
            py::init<>(),
            // the docstring
            "the empty interval");
        // the interval between two points
        cls.def(
            // the constructor
            py::init<const point_t &, const point_t &>(),
            // the signature
            "lower"_a, "upper"_a,
            // the docstring
            "the points from {lower} to {upper}, both included; empty when they are out of order");
        // the whole line
        cls.def_static(
            // the name
            "line",
            // the implementation
            &interval_t::line,
            // the docstring
            "the whole line");

        // the lower end
        cls.def_property_readonly(
            // the name
            "lower",
            // the implementation
            &interval_t::lower,
            // the docstring
            "my lower end");
        // the upper end
        cls.def_property_readonly(
            // the name
            "upper",
            // the implementation
            &interval_t::upper,
            // the docstring
            "my upper end");
        // whether it holds anything
        cls.def_property_readonly(
            // the name
            "empty",
            // the implementation
            &interval_t::empty,
            // the docstring
            "whether i hold no points");
        // whether it has a lower end on the line
        cls.def_property_readonly(
            // the name
            "boundedBelow",
            // the implementation
            &interval_t::boundedBelow,
            // the docstring
            "whether my lower end is on the line");
        // whether it has an upper end on the line
        cls.def_property_readonly(
            // the name
            "boundedAbove",
            // the implementation
            &interval_t::boundedAbove,
            // the docstring
            "whether my upper end is on the line");

        // whether it holds a point
        cls.def(
            // the name
            "contains",
            // the implementation
            &interval_t::contains,
            // the signature
            "point"_a,
            // the docstring
            "check whether i hold {point}");
        // the smallest interval that holds it
        cls.def(
            // the name
            "envelope",
            // the implementation
            &interval_t::envelope,
            // the docstring
            "the smallest interval that holds me");

        // whether it shares a point with another interval
        cls.def(
            // the name
            "intersects",
            // the implementation
            [](const interval_t & self, const interval_t & other) {
                // ask the relation
                return pyre::geometry::intersects(self, other);
            },
            // the signature
            "other"_a,
            // the docstring
            "check whether i share a point with {other}");
        // or with a union
        cls.def(
            // the name
            "intersects",
            // the implementation
            [](const interval_t & self, const union_t & other) {
                // ask the relation
                return pyre::geometry::intersects(self, other);
            },
            // the signature
            "other"_a,
            // the docstring
            "check whether i share a point with {other}");
        // whether it covers another interval
        cls.def(
            // the name
            "covers",
            // the implementation
            [](const interval_t & self, const interval_t & other) {
                // ask the relation
                return pyre::geometry::covers(self, other);
            },
            // the signature
            "other"_a,
            // the docstring
            "check whether every point of {other} is one of mine");
        // or a union
        cls.def(
            // the name
            "covers",
            // the implementation
            [](const interval_t & self, const union_t & other) {
                // ask the relation
                return pyre::geometry::covers(self, other);
            },
            // the signature
            "other"_a,
            // the docstring
            "check whether every point of {other} is one of mine");

        // two intervals compare equal when they hold the same points
        cls.def(py::self == py::self);

        // a readable representation
        cls.def(
            // the name
            "__repr__",
            // the handler lets the interval write itself
            [](const interval_t & interval) {
                // make a buffer
                auto buffer = std::ostringstream {};
                // write the interval
                buffer << interval;
                // and hand off its contents
                return buffer.str();
            });

        // all done
        return;
    }
} // namespace pyre::py::geometry


// bind the intervals
void
pyre::py::geometry::interval(py::module & m)
{
    // the intervals of the lines
    lineInterval<timeline_t>(m, "TimelineInterval", "a closed interval of the timeline");

    // all done
    return;
}


// end of file
