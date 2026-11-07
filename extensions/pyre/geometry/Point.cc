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
    // bind the points of a line, which are known by their coordinates along it
    template <class lineT>
    inline void linePoint(py::module & m, classname_t name, docstring_t docstring)
    {
        // the point
        using point_t = pyre::geometry::point_t<lineT>;

        // wrap it
        auto cls = py::class_<point_t>(
            // the scope
            m,
            // the name of the class
            name,
            // its docstring
            docstring);

        // the coordinate of the point
        cls.def_property_readonly(
            // the name
            "coordinate",
            // the implementation asks the line
            [](const point_t & point) { return lineT::coordinate(point.data()); },
            // the docstring
            "my coordinate along the line");

        // two points compare equal when they are the same point
        cls.def(py::self == py::self);

        // a readable representation
        cls.def(
            // the name
            "__repr__",
            // the handler lets the line write the point
            [](const point_t & point) {
                // make a buffer
                auto buffer = std::ostringstream {};
                // write the point
                buffer << point;
                // and hand off its contents
                return buffer.str();
            });

        // all done
        return;
    }
} // namespace pyre::py::geometry


// bind the points
void
pyre::py::geometry::point(py::module & m)
{
    // the points of the lines
    linePoint<timeline_t>(m, "TimelinePoint", "an instant, known by its seconds since the epoch");

    // all done
    return;
}


// end of file
