// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the bitmap image products
void
pyre::py::viz::images(py::module & m)
{
    // register them with the catalog
    pyre::py::flow::registry().registerProduct<image_t>();

    // bind them
    auto cls = py::classh<image_t, pyre::py::flow::product_t>(
        // the scope
        m,
        // the name of the class
        "Image",
        // the docstring
        "a microsoft bitmap, as a product of a flow graph");
    // its shape
    cls.def_property_readonly(
        // the name
        "shape",
        // the implementation
        [](const image_t & self) -> std::tuple<int, int> {
            // get the shape
            auto shape = self.shape();
            // and hand off its extents
            return { shape[0], shape[1] };
        },
        // the docstring
        "my shape");
    // its bytes
    cls.def(
        // the name
        "read",
        // the implementation
        [](image_t & self) -> py::bytes {
            // pull my bytes, refreshing them if they are stale
            auto view = self.read();
            // and hand off a copy
            return py::bytes(reinterpret_cast<const char *>(view.data()), view.cells());
        },
        // the docstring
        "refresh me if i am stale, and hand off a copy of my bytes, headers and all");

    // all done
    return;
}


// end of file
