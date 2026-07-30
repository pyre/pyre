// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// dataset creation property lists
void
pyre::h5::py::properties::dcpl(py::module & m)
{
    // add bindings for hdf5 dataset creation property lists
    auto cls = py::class_<DCPL, PropList>(
        // in scope
        m,
        // class name
        "dcpl",
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

    // set the fill value
    cls.def(
        // the name
        "setFillValue",
        // the implementation
        [](DCPL & self, const py::object & value) -> void {
            // integers travel as 64-bit
            if (py::isinstance<py::int_>(value)) {
                // convert
                auto v = value.cast<std::int64_t>();
                // and deposit; hdf5 converts to the dataset's on-disk type at creation
                self.setFillValue(pyre::h5::datatype<std::int64_t>(), &v);
                // all done
                return;
            }
            // floats as doubles
            if (py::isinstance<py::float_>(value)) {
                // convert
                auto v = value.cast<double>();
                // and deposit
                self.setFillValue(pyre::h5::datatype<double>(), &v);
                // all done
                return;
            }
            // anything else must be a complex number; the cast raises if it isn't
            auto v = value.cast<std::complex<double>>();
            // deposit
            self.setFillValue(pyre::h5::datatype<std::complex<double>>(), &v);
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "set the fill value; hdf5 converts it to the dataset's on-disk type at creation");

    // get the fill value
    cls.def(
        // the name
        "fillValue",
        // the implementation
        [](const DCPL & self, const string_t & cell) -> py::object {
            // as a 64-bit integer
            if (cell == "int64") {
                // make room
                std::int64_t v = 0;
                // read it
                self.fillValue(pyre::h5::datatype<std::int64_t>(), &v);
                // and lift it into python
                return py::cast(v);
            }
            // as a double
            if (cell == "float64") {
                // make room
                double v = 0;
                // read it
                self.fillValue(pyre::h5::datatype<double>(), &v);
                // and lift it into python
                return py::cast(v);
            }
            // as a complex double
            if (cell == "complex128") {
                // make room
                std::complex<double> v = 0;
                // read it
                self.fillValue(pyre::h5::datatype<std::complex<double>>(), &v);
                // and lift it into python
                return py::cast(v);
            }
            // anything else is a caller mistake
            throw py::value_error("unsupported fill value cell type '" + cell + "'");
        },
        // the signature
        "cell"_a = "float64",
        // the docstring
        "get the fill value, interpreted as the given {cell} type");

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
