// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// bitmap bindings
void
pyre::py::viz::bmp(py::module & m)
{
    // turn {pyre::viz::bmp_t} into a {buffer}
    auto bmp = py::class_<bmp_t>(
        // the scope
        m,
        // the name of the class
        "BMP",
        // decorations
        py::buffer_protocol());

    // add the buffer constructor
    bmp.def_buffer(
        // the handler
        [](const bmp_t & bitmap) -> py::buffer_info {
            // build one and return it
            return py::buffer_info(
                // the pointer
                bitmap.data(),
                // the size of each individual entry
                sizeof(bmp_t::byte_type),
                // the format
                py::format_descriptor<bmp_t::byte_type>::format(),
                // ??
                1,
                // the total size of the bitmap, in bytes
                { bitmap.bytes() },
                // ??
                { 1 });
        });

    // all done
    return;
}


// end of file
