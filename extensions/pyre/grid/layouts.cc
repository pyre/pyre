// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// my implementations
#include "layouts.h"


// wrappers over {pyre::grid::canonical_t} template expansions
// build the submodule
void
pyre::py::grid::layouts(py::module & m)
{
    // instantiate layouts of a few dimensions
    canonical2d(m);
    canonical3d(m);
    canonical4d(m);

    // all done
    return;
}


// layout instantiations
void
pyre::py::grid::canonical2d(py::module & m)
{
    // type alias
    using layout_t = pyre::grid::canonical_t<2>;

    // build the class record
    auto cls = py::class_<layout_t>(
        // in scope
        m,
        // class name
        "Canonical2D",
        // docstring
        "a 2d canonical layout");

    // add the layout interface
    layoutInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::canonical3d(py::module & m)
{
    // type alias
    using layout_t = pyre::grid::canonical_t<3>;

    // build the class record
    auto cls = py::class_<layout_t>(
        // in scope
        m,
        // class name
        "Canonical3D",
        // docstring
        "a 3d canonical layout");

    // add the layout interface
    layoutInterface(cls);

    // all done
    return;
}


void
pyre::py::grid::canonical4d(py::module & m)
{
    // type alias
    using layout_t = pyre::grid::canonical_t<4>;

    // build the class record
    auto cls = py::class_<layout_t>(
        // in scope
        m,
        // class name
        "Canonical4D",
        // docstring
        "a 4d canonical layout");

    // add the layout interface
    layoutInterface(cls);

    // all done
    return;
}


// the interface decorator
template <class layoutT>
void
pyre::py::grid::layoutInterface(py::class_<layoutT> & cls)
{
    // constructors
    cls.def(
        // the constructor
        py::init<typename layoutT::shape_const_reference>(),
        // the signature
        "shape"_a,
        // the docstring
        "create a layout from the given {shape}");

    cls.def(
        // the constructor
        py::init<
            typename layoutT::shape_const_reference, typename layoutT::index_const_reference>(),
        // the signature
        "shape"_a, "origin"_a,
        // the docstring
        "create a layout from the given {shape} starting at {origin}");

    cls.def(
        // the constructor
        py::init<
            typename layoutT::shape_const_reference, typename layoutT::index_const_reference,
            typename layoutT::order_const_reference>(),
        // the signature
        "shape"_a, "origin"_a, "order"_a,
        // the docstring
        "create a layout from the given {shape} and packing {order} starting at {origin}");

    // accessors
    cls.def_property_readonly_static(
        // the name of the property
        "rank",
        // the implementation
        [](py::object) {
            // get my rank and return it
            return layoutT::rank();
        },
        // the docstring
        "my rank");

    cls.def_property_readonly(
        // the name of the property
        "shape",
        // the accessor
        &layoutT::shape,
        // the docstring
        "get my shape");

    cls.def_property_readonly(
        // the name of the property
        "origin",
        // the accessor
        &layoutT::origin,
        // the docstring
        "get my origin");

    cls.def_property_readonly(
        // the name of the property
        "order",
        // the accessor
        [](const layoutT & self) -> typename layoutT::order_type { return self.order(); },
        // the docstring
        "get my order");

    cls.def_property_readonly(
        // the name of the property
        "strides",
        // the accessor
        &layoutT::strides,
        // the docstring
        "get my strides");

    cls.def_property_readonly(
        // the name of the property
        "nudge",
        // the accessor
        &layoutT::nudge,
        // the docstring
        "get my nudge");

    // interface
    cls.def(
        // the name of the method
        "index",
        // the implementation
        &layoutT::index,
        // the signature
        "offset"_a,
        // the docstring
        "compute the index that corresponds to {offset}");

    cls.def(
        // the name of the method
        "offset",
        // the implementation
        &layoutT::offset,
        // the signature
        "index"_a,
        // the docstring
        "compute the offset that corresponds to {index}");

    // slicing
    cls.def(
        // the name of the method
        "box",
        // the implementation
        &layoutT::box,
        // the signature
        "origin"_a, "shape"_a,
        // the doctring
        "make a layout that is restricted to the given {shape} starting at the given {origin}");

    // metamethods
    // iterators
    cls.def(
        // the name of the method
        "__iter__",
        // the implementation
        [](const layoutT & layout) {
            // make an iterator and return it
            return py::make_iterator(layout.begin(), layout.end());
        },
        // make sure it lives long enough
        py::keep_alive<0, 1>(),
        // docstring
        "make an iterator");

    // all done
    return;
}


// end of file
