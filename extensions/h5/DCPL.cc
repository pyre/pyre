// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


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
        [](const py::object &) -> const DCPL & {
            // easy enough
            return DCPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
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
        &DCPL::allocTime,
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
        &DCPL::chunk,
        // the signature
        "rank"_a,
        // the docstring
        "get the chunk size given the dataset {rank}");
    // set the chunk size
    cls.def(
        // the name
        "setChunk",
        // the implementation
        &DCPL::setChunk,
        // the signature
        "shape"_a,
        // the docstring
        "set the chunk {shape}");

    // get the fill value writing time
    cls.def(
        // the name
        "getFillTime",
        // the implementation
        &DCPL::fillTime,
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
        &DCPL::layout,
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

    // filters
    cls.def(
        // the name
        "getFilters",
        // the implementation
        &DCPL::filters,
        // the docstring
        "get the filters in the dataset pipeline");

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
    // shuffle
    cls.def(
        // the name
        "setShuffle",
        // the implementation
        &DCPL::setShuffle,
        // the docstring
        "use the shuffle filter to improve compression");
    // fletcher32
    cls.def(
        // the name
        "setFletcher32",
        // the implementation
        &DCPL::setFletcher32,
        // the docstring
        "use the fletcher32 checksum filter for error detection");
    // scaleoffset
    cls.def(
        // the name
        "setScaleoffset",
        // the implementation
        &DCPL::setScaleoffset,
        // the signature
        "scaleType"_a, "scaleFactor"_a,
        // the docstring
        "use the scale-offset filter with the given {scaleType} and {scaleFactor}");


    // all done
    return;
}


// end of file
