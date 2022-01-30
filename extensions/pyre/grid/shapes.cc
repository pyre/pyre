// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


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

    // all done
    return;
}


// shapes
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

    // add the accessors
    reps(cls);
    // install the algebra
    algebra(cls);

    // all done
    return;
}


// end of file
