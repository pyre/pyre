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
    auto cls = py::class_<DCPL, OCPL>(
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
    // the allocation time
    cls.def_property(
        // the name
        "allocTime",
        // the getter
        &DCPL::allocTime,
        // the setter
        &DCPL::setAllocTime,
        // the docstring
        "when storage is allocated for the dataset");

    // the chunk shape
    cls.def_property(
        // the name
        "chunk",
        // the getter
        &DCPL::chunk,
        // the setter
        &DCPL::setChunk,
        // the docstring
        "the shape of my chunks; empty when my layout is not chunked");

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
    cls.def_property(
        // the name
        "fillTime",
        // the getter
        &DCPL::fillTime,
        // the setter
        &DCPL::setFillTime,
        // the docstring
        "when the fill value is written to storage");
    // set the fill value writing time


    // get the data layout strategy
    cls.def_property(
        // the name
        "layout",
        // the getter
        &DCPL::layout,
        // the setter
        &DCPL::setLayout,
        // the docstring
        "how my cells are laid out in storage");


    // filters; the pipeline is read-only because filters are engaged one at a time, in
    // the order they are to be applied
    cls.def_property_readonly(
        // the name
        "filters",
        // the getter
        &DCPL::filters,
        // the docstring
        "the filters in my pipeline, in the order they are applied");

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
