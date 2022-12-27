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
#include "indices.h"


// wrappers over {pyre::grid::index_t} template expansions
// build the submodule
void
pyre::py::grid::indices(py::module & m)
{
    // instantiate indices of a few dimensions
    index2d(m);
    index3d(m);
    index4d(m);

    // all done
    return;
}


// index instantiations
void
pyre::py::grid::index2d(py::module & m)
{
    // type alias
    using index_t = pyre::grid::index_t<2>;

    // build the class record
    auto cls = py::class_<index_t>(
        // in scope
        m,
        // class name
        "Index2D",
        // docstring
        "a 2d index specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int> index) {
            // unpack
            auto [s1, s2] = index;
            // instantiate
            return new index_t(s1, s2);
        }),
        // the docstring
        "create an index",
        // the signature: a pair of integers
        "index"_a);

    // add the index interface
    indexInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::index3d(py::module & m)
{
    // type alias
    using index_t = pyre::grid::index_t<3>;

    // build the class record
    auto cls = py::class_<index_t>(
        // in scope
        m,
        // class name
        "Index3D",
        // docstring
        "a 3d index specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int, int> index) {
            // unpack
            auto [s1, s2, s3] = index;
            // instantiate
            return new index_t(s1, s2, s3);
        }),
        // the docstring
        "create an index",
        // the signature: a tuple of 3 integers
        "index"_a);

    // add the index interface
    indexInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::index4d(py::module & m)
{
    // type alias
    using index_t = pyre::grid::index_t<4>;

    // build the class record
    auto cls = py::class_<index_t>(
        // in scope
        m,
        // class name
        "Index4D",
        // docstring
        "a 4d index specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int, int, int> index) {
            // unpack
            auto [s1, s2, s3, s4] = index;
            // instantiate
            return new index_t(s1, s2, s3, s4);
        }),
        // the docstring
        "create an index",
        // the signature: a tuple of 4 integers
        "index"_a);

    // add the index interface
    indexInterface(cls);

    // all done
    return;
}


// the interface decorator
template <class indexT>
void
pyre::py::grid::indexInterface(py::class_<indexT> & cls)
{

    // add the filling constructor
    cls.def(
        // the constructor
        py::init([](typename indexT::rank_type value) {
            // instantiate and return
            return new indexT(value);
        }),
        // the docstring
        "create an index filled with {value}",
        // the signature: a tuple of 4 integers
        "value"_a);

    // add the accessors from {pyre::grid::rep_t}
    reps(cls);
    // install the algebra
    algebra(cls);

    // all done
    return;
}

// end of file
