// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the bindings of the relations between shapes, as functions of the module and as methods of the
// shapes; each pair of kinds gets the relations the library has for it, and nothing else
namespace pyre::py::geometry {
    // bind {intersects} and {covers} between shapes of the kinds {firstT} and {secondT} as
    // functions of the module {m}
    template <class firstT, class secondT>
    inline void relate(py::module & m)
    {
        // when the pair shares points, in either order
        if constexpr (requires(const firstT & a, const secondT & b) {
                          pyre::geometry::intersects(a, b);
                      }) {
            // bind it
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
        }
        // when the first may cover the second
        if constexpr (requires(const firstT & a, const secondT & b) {
                          pyre::geometry::covers(a, b);
                      }) {
            // bind it
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
        }
        // all done
        return;
    }

    // bind the relations between the shapes of the kind {firstT} and each of the kinds in
    // {otherT} as functions of the module {m}
    template <class firstT, class... otherT>
    inline void relateWith(py::module & m)
    {
        // one kind at a time
        (relate<firstT, otherT>(m), ...);
        // all done
        return;
    }

    // bind the relations between every pair of shapes of the kinds in {shapeT}, in both orders,
    // as functions of the module {m}
    template <class... shapeT>
    inline void relateAll(py::module & m)
    {
        // each kind against all of them
        (relateWith<shapeT, shapeT...>(m), ...);
        // all done
        return;
    }

    // bind {intersects} and {covers} against shapes of the kind {otherT} as methods of {cls},
    // the class of the shapes of the kind {selfT}
    template <class selfT, class otherT>
    inline void relateMethod(py::class_<selfT> & cls)
    {
        // when the pair shares points, in either order
        if constexpr (requires(const selfT & self, const otherT & other) {
                          pyre::geometry::intersects(self, other);
                      }) {
            // bind it
            cls.def(
                // the name
                "intersects",
                // the implementation
                [](const selfT & self, const otherT & other) {
                    // ask the relation
                    return pyre::geometry::intersects(self, other);
                },
                // the signature
                "other"_a,
                // the docstring
                "check whether i share a point with {other}");
        }
        // when the shape may cover the other one
        if constexpr (requires(const selfT & self, const otherT & other) {
                          pyre::geometry::covers(self, other);
                      }) {
            // bind it
            cls.def(
                // the name
                "covers",
                // the implementation
                [](const selfT & self, const otherT & other) {
                    // ask the relation
                    return pyre::geometry::covers(self, other);
                },
                // the signature
                "other"_a,
                // the docstring
                "check whether every point of {other} is one of mine");
        }
        // all done
        return;
    }

    // bind the relations of {cls} against shapes of every one of the kinds {otherT}
    template <class selfT, class... otherT>
    inline void relateMethods(py::class_<selfT> & cls)
    {
        // one kind at a time
        (relateMethod<selfT, otherT>(cls), ...);
        // all done
        return;
    }
} // namespace pyre::py::geometry


// end of file
