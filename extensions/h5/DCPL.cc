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
        [](const DCPL & self, int rank) {
            // make a vector big enough to hold the answer
            shape_t shape(rank);
            // get the chunk size
            self.getChunk(rank, &shape[0]);
            // and return it
            return shape;
        },
        // the signature
        "rank"_a,
        // the docstring
        "get the chunk size given the dataset {rank}");
    // set the chunk size
    cls.def(
        // the name
        "setChunk",
        // the implementation
        [](const DCPL & self, const shape_t & shape) -> void {
            // set the chunk size and shape
            self.setChunk(shape.size(), &shape[0]);
            // all done
            return;
        },
        // the signature
        "shape"_a,
        // the docstring
        "set the chunk {shape}");

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

    // filters
    cls.def(
        // the name
        "getFilters",
        // the implementation
        [](const DCPL & self) {
            // the filter info
            using filter_info_t = std::tuple<H5Z_filter_t, string_t, unsigned int, unsigned int>;
            // make a pile
            auto filters = std::vector<filter_info_t>();

            // go through the registered filters
            for (int i = 0; i < self.getNfilters(); ++i) {
                // make some room
                unsigned int flags;
                char name[256];
                size_t clientDataElements = 0;
                unsigned int * clientDataValues = nullptr;
                unsigned int configuration;
                // get the info
                auto id = self.getFilter(
                    i, flags, clientDataElements, clientDataValues, sizeof(name), name,
                    configuration);
                // store
                filters.emplace_back(id, name, flags, configuration);
            }
            // all done
            return filters;
        },
        // the docstring
        "get the number of filters in the dataset pipeline");

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
