// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// my implementations
// arithmetic
#include "algebra.h"
// basic accessors
#include "reps.h"
// constructors
#include "shapes.h"


// wrappers over {pyre::grid::shape_t} template expansions
// build the submodule
void
pyre::py::grid::shapes(py::module & m)
{
    // instantiate shapes of a few dimensions
    shape2d(m);
    shape3d(m);
    shape4d(m);

    // all done
    return;
}


// shape instantiations
void
pyre::py::grid::shape2d(py::module & m)
{
    // type alias
    using shape_t = pyre::grid::shape_t<2>;

    // build the class record
    auto cls = py::class_<shape_t>(
        // in scope
        m,
        // class name
        "Shape2D",
        // docstring
        "a 2d shape specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int> shape) {
            // unpack
            auto [s1, s2] = shape;
            // instantiate
            return new shape_t(s1, s2);
        }),
        // the docstring
        "create a shape",
        // the signature: a pair of integers
        "shape"_a);

    // add the shape interface
    shapeInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::shape3d(py::module & m)
{
    // type alias
    using shape_t = pyre::grid::shape_t<3>;

    // build the class record
    auto cls = py::class_<shape_t>(
        // in scope
        m,
        // class name
        "Shape3D",
        // docstring
        "a 3d shape specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int, int> shape) {
            // unpack
            auto [s1, s2, s3] = shape;
            // instantiate
            return new shape_t(s1, s2, s3);
        }),
        // the docstring
        "create a shape",
        // the signature: a tuple of 3 integers
        "shape"_a);

    // add the shape interface
    shapeInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::shape4d(py::module & m)
{
    // type alias
    using shape_t = pyre::grid::shape_t<4>;

    // build the class record
    auto cls = py::class_<shape_t>(
        // in scope
        m,
        // class name
        "Shape4D",
        // docstring
        "a 4d shape specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int, int, int> shape) {
            // unpack
            auto [s1, s2, s3, s4] = shape;
            // instantiate
            return new shape_t(s1, s2, s3, s4);
        }),
        // the docstring
        "create a shape",
        // the signature: a tuple of 4 integers
        "shape"_a);

    // add the shape interface
    shapeInterface(cls);

    // all done
    return;
}


// the interface decorator
template <class shapeT>
void
pyre::py::grid::shapeInterface(py::class_<shapeT> & cls)
{
    // add the accessors from {pyre::grid::rep_t}
    reps(cls);
    // install the algebra
    algebra(cls);

    // cells
    cls.def_property_readonly(
        // the name of the method
        "cells",
        // the implementation
        &shapeT::cells,
        // the docstring
        "the total number of addressable values");

    // all done
    return;
}

// end of file
