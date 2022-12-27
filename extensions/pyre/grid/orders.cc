// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// my implementations
#include "orders.h"


// wrappers over {pyre::grid::order_t} template expansions
// build the submodule
void
pyre::py::grid::orders(py::module & m)
{
    // instantiate orders of a few dimensions
    order2d(m);
    order3d(m);
    order4d(m);

    // all done
    return;
}


// order instantiations
void
pyre::py::grid::order2d(py::module & m)
{
    // type alias
    using order_t = pyre::grid::order_t<2>;

    // build the class record
    auto cls = py::class_<order_t>(
        // in scope
        m,
        // class name
        "Order2D",
        // docstring
        "a 2d order specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int> order) {
            // unpack
            auto [s1, s2] = order;
            // instantiate
            return new order_t(s1, s2);
        }),
        // the docstring
        "create a order",
        // the signature: a pair of integers
        "order"_a);

    // add the order interface
    orderInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::order3d(py::module & m)
{
    // type alias
    using order_t = pyre::grid::order_t<3>;

    // build the class record
    auto cls = py::class_<order_t>(
        // in scope
        m,
        // class name
        "Order3D",
        // docstring
        "a 3d order specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int, int> order) {
            // unpack
            auto [s1, s2, s3] = order;
            // instantiate
            return new order_t(s1, s2, s3);
        }),
        // the docstring
        "create a order",
        // the signature: a tuple of 3 integers
        "order"_a);

    // add the order interface
    orderInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::order4d(py::module & m)
{
    // type alias
    using order_t = pyre::grid::order_t<4>;

    // build the class record
    auto cls = py::class_<order_t>(
        // in scope
        m,
        // class name
        "Order4D",
        // docstring
        "a 4d order specification");

    // add the constructor
    cls.def(
        // the constructor
        py::init([](std::tuple<int, int, int, int> order) {
            // unpack
            auto [s1, s2, s3, s4] = order;
            // instantiate
            return new order_t(s1, s2, s3, s4);
        }),
        // the docstring
        "create a order",
        // the signature: a tuple of 4 integers
        "order"_a);

    // add the order interface
    orderInterface(cls);

    // all done
    return;
}


// the interface decorator
template <class orderT>
void
pyre::py::grid::orderInterface(py::class_<orderT> & cls)
{
    // factories
    cls.def_static(
        // the name of the function
        "c",
        // the implementation
        []() -> orderT {
            // easy enough...
            return orderT::c();
        },
        // the docstring
        "create a row major ordering");

    cls.def_static(
        // the name of the function
        "rowMajor",
        // the implementation
        []() -> orderT {
            // easy enough...
            return orderT::rowMajor();
        },
        // the docstring
        "create a row major ordering");

    cls.def_static(
        // the name of the function
        "fortran",
        // the implementation
        []() -> orderT {
            // easy enough...
            return orderT::fortran();
        },
        // the docstring
        "create a column major ordering");

    cls.def_static(
        // the name of the function
        "columnMajor",
        // the implementation
        []() -> orderT {
            // easy enough...
            return orderT::columnMajor();
        },
        // the docstring
        "create a column major ordering");

    // access to individual ranks
    cls.def(
        // the name of the method
        "__getitem__",
        // the implementation
        [](const orderT & self, int index) -> int {
            // access the requested rank and return its value
            return self[index];
        },
        // the signature
        "index"_a,
        // docstring
        "get the value at the specified {index}");

    // iterator
    cls.def(
        // the name of the method
        "__iter__",
        // the implementation
        [](const orderT & order) {
            // make an iterator and return it
            return py::make_iterator(order.cbegin(), order.cend());
        },
        // make sure it lives long enough
        py::keep_alive<0, 1>(),
        // docstring
        "make an iterator");

    // all done
    return;
}

// end of file
