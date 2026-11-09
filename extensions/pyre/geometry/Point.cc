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
    // register the class of the points of a line, so that every signature can name it
    template <class lineT>
    inline void linePointClass(py::module & m, classname_t name, docstring_t docstring)
    {
        // register the point
        py::class_<pyre::geometry::point_t<lineT>>(
            // the scope
            m,
            // the name of the class
            name,
            // its docstring
            docstring);

        // all done
        return;
    }

    // bind the points of a line, which are known by their coordinates along it
    template <class lineT>
    inline void linePoint()
    {
        // the point
        using point_t = pyre::geometry::point_t<lineT>;

        // the class of the point, registered by {linePointClass}
        auto cls = py::class_<point_t>(py::type::of<point_t>());

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


// register the classes of the points, so that every signature can name them
void
pyre::py::geometry::pointClasses(py::module & m)
{
    // the points of the lines
    linePointClass<timeline_t>(
        m, "TimelinePoint", "an instant, known by its seconds since the epoch");
    // the points of the sphere, which are named by the charts
    py::class_<place_t>(
        // the scope
        m,
        // the name of the class
        "SpherePoint",
        // its docstring
        "a point of the sphere, the unit vector of its direction from the center");

    // all done
    return;
}


// bind the points
void
pyre::py::geometry::point()
{
    // the points of the lines
    linePoint<timeline_t>();

    // the class of the points of the sphere, registered by {pointClasses}
    auto cls = py::class_<place_t>(py::type::of<place_t>());
    // two points compare equal when they are the same point
    cls.def(py::self == py::self);
    // a readable representation
    cls.def(
        // the name
        "__repr__",
        // the handler lets the sphere write the point
        [](const place_t & point) {
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


// end of file
