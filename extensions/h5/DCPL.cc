// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// dataset creation property lists
void
pyre::h5::py::dcpl(py::module & m)
{
    // add bindings for hdf5 dataset creation property lists
    auto cls = py::class_<DCPL, PropList>(
        // in scope
        m,
        // class name
        "DCPL",
        // docstring
        "a dataset creation property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) {
            // easy enough
            return &DCPL::DEFAULT;
        },
        // docstring
        "the default dataset creation property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a dataset creation property list");

    // interface
    // get the allocation time
    cls.def(
        // the name
        "getAllocTime",
        // the implementation
        &DCPL::getAllocTime,
        // the docstring
        "get the allocation time");
    // set the allocation time
    cls.def(
        // the name
        "setAllocTime",
        // the implementation
        &DCPL::setAllocTime,
        // the signature
        "timing"_a,
        // the docstring
        "set the allocation time");

    // get the chunk size
    cls.def(
        // the name
        "getChunk",
        // the implementation
        &DCPL::getChunk,
        // the docstring
        "get the chunk size");
    // set the chunk size
    cls.def(
        // the name
        "setChunk",
        // the implementation
        [](const DCPL & self, const shape_t & chunk) -> void {
            // set the chunk size and shape
            self.setChunk(chunk.size(), &chunk[0]);
            // all done
            return;
        },
        // the signature
        "chunk"_a,
        // the docstring
        "set the chunk size");

    // get the fill value writing time
    cls.def(
        // the name
        "getFillTime",
        // the implementation
        &DCPL::getFillTime,
        // the docstring
        "get the fill value writing time");
    // set the fill value writing time
    cls.def(
        // the name
        "setFillTime",
        // the implementation
        &DCPL::setFillTime,
        // the signature
        "timing"_a,
        // the docstring
        "set the fill value writing time");

    // get the data layout strategy
    cls.def(
        // the name
        "getLayout",
        // the implementation
        &DCPL::getLayout,
        // the docstring
        "get the data layout strategy");
    // set the data layout strategy
    cls.def(
        // the name
        "setLayout",
        // the implementation
        &DCPL::setLayout,
        // the signature
        "layout"_a,
        // the docstring
        "set the data layout strategy");

    // compression
    // deflate
    cls.def(
        // the name
        "setDeflate",
        // the implementation
        &DCPL::setDeflate,
        // the signature
        "level"_a,
        // the docstring
        "use deflate with the given {level}");
    // szip
    cls.def(
        // the name
        "setSzip",
        // the implementation
        &DCPL::setSzip,
        // the signature
        "options"_a, "pixelsPerBlock"_a,
        // the docstring
        "use szip compression with the given {options} and {pixelsPerBlock}");
    // nbit
    cls.def(
        // the name
        "setNbit",
        // the implementation
        &DCPL::setNbit,
        // the docstring
        "use nbit compression");


    // all done
    return;
}


// end of file
