// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// dataset access property lists
void
pyre::h5::py::dapl(py::module & m)
{
    // add bindings for hdf5 dataset access property lists
    auto cls = py::class_<DAPL, PropList>(
        // in scope
        m,
        // class name
        "DAPL",
        // docstring
        "a dataset access property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) {
            // easy enough
            return &DAPL::DEFAULT;
        },
        // docstring
        "the default dataset access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a dataset access property list");

    // interface
    // get the chunk size
    cls.def(
        // the name
        "getChunkCache",
        // the implementation
        [](const DAPL & self) {
            // make some room
            size_t slots;
            size_t bytes;
            double w0;
            // get the values
            self.getChunkCache(slots, bytes, w0);
            // pack and ship
            return py::make_tuple(slots, bytes, w0);
        },
        // the docstring
        "get the chunk cache parameters");
    // set the chunk size
    cls.def(
        // the name
        "setChunkCache",
        // the implementation
        [](const DAPL & self, size_t slots, size_t bytes, double w0) -> void {
            // set the chunk size and shape
            self.setChunkCache(slots, bytes, w0);
            // all done
            return;
        },
        // the signature
        "slots"_a, "bytes"_a, "w0"_a,
        // the docstring
        "set the chunk cache parameters");


    // all done
    return;
}


// end of file
