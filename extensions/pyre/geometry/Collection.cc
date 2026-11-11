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


// helpers
namespace pyre::py::geometry {
    // register the class of the finite unions of a kind of shape, so that every signature can
    // name it
    template <class shapeT>
    inline void shapeCollectionClass(py::module & m, classname_t name, docstring_t docstring)
    {
        // register the union
        py::class_<pyre::geometry::collection_t<shapeT>>(
            // the scope
            m,
            // the name of the class
            name,
            // its docstring
            docstring);

        // all done
        return;
    }

    // bind the finite unions of a kind of shape, related to the shapes of that kind, to each
    // other, and to the shapes of the kinds in {otherT}
    template <class shapeT, class... otherT>
    inline void shapeCollection()
    {
        // the union
        using union_t = pyre::geometry::collection_t<shapeT>;
        // and its members
        using shapes_t = typename union_t::shapes_type;

        // the class of the union, registered by {shapeCollectionClass}
        auto cls = py::class_<union_t>(py::type::of<union_t>());

        // the union of the given shapes
        cls.def(
            // the constructor
            py::init<shapes_t>(),
            // the signature
            "shapes"_a,
            // the docstring
            "the union of {shapes}");

        // the number of members
        cls.def(
            // the name
            "__len__",
            // the implementation
            &union_t::size,
            // the docstring
            "the number of my members");
        // the members, in the order they were given
        cls.def(
            // the name
            "__iter__",
            // the implementation
            [](const union_t & self) { return py::make_iterator(self.begin(), self.end()); },
            // the union outlives the iteration
            py::keep_alive<0, 1>(),
            // the docstring
            "iterate over my members");
        // the smallest envelope that holds every member
        cls.def(
            // the name
            "envelope",
            // the implementation
            &union_t::envelope,
            // the docstring
            "the smallest envelope that holds all my members");

        // the relations with shapes of the kind of its members, with other unions, and with the
        // other kinds of shapes it can be compared with
        relateMethods<union_t, shapeT, union_t, otherT...>(cls);

        // two unions compare equal when they have the same members in the same order
        cls.def(py::self == py::self);
        // and equal unions hash alike, so they can be members of sets and keys of dicts
        cls.def(
            // the name
            "__hash__",
            // the implementation
            &union_t::hash,
            // the docstring
            "my hash, shared by the unions that compare equal");

        // a readable representation, for the shapes that can write themselves
        if constexpr (requires(std::ostream & stream, const shapeT & shape) { stream << shape; }) {
            cls.def(
                // the name
                "__repr__",
                // the handler writes the members, joined by the union sign
                [](const union_t & self) {
                    // the union of nothing
                    if (self.size() == 0) {
                        // is the empty set
                        return string_t("{}");
                    }
                    // make a buffer
                    auto buffer = std::ostringstream {};
                    // the separator goes between members, so there is none before the first one
                    auto separator = "";
                    // go through the members
                    for (const auto & shape : self) {
                        // and write each one after the separator
                        buffer << separator << shape;
                        // and use the union sign from now on
                        separator = " ∪ ";
                    }
                    // hand off the contents
                    return buffer.str();
                });
        }

        // all done
        return;
    }
} // namespace pyre::py::geometry


// register the classes of the unions, so that every signature can name them
void
pyre::py::geometry::collectionClasses(py::module & m)
{
    // the unions of intervals
    shapeCollectionClass<interval_t>(
        m, "TimelineIntervals", "a finite union of intervals of the timeline");
    // the unions of polygons on the sphere
    shapeCollectionClass<polygon_t>(
        m, "SpherePolygons", "a finite union of polygons on the sphere");

    // all done
    return;
}


// bind the unions
void
pyre::py::geometry::collection()
{
    // the unions of intervals
    shapeCollection<interval_t>();
    // the unions of polygons on the sphere
    shapeCollection<polygon_t, place_t, box_t, path_t>();

    // all done
    return;
}


// end of file
