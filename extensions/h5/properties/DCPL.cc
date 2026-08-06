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
        py::overload_cast<>(&DCPL::allocTime, py::const_),
        // the setter
        py::overload_cast<H5D_alloc_time_t>(&DCPL::allocTime),
        // the docstring
        "when storage is allocated for the dataset");

    // the chunk shape
    cls.def_property(
        // the name
        "chunk",
        // the getter
        py::overload_cast<>(&DCPL::chunk, py::const_),
        // the setter
        py::overload_cast<const shape_t &>(&DCPL::chunk),
        // the docstring
        "the shape of my chunks; empty when my layout is not chunked");

    // whether a fill value was ever declared, and by whom
    cls.def_property_readonly(
        // the name
        "fillValueStatus",
        // the implementation
        &DCPL::fillValueStatus,
        // the docstring
        "whether a fill value is defined, and whether it is mine or the library's default");

    // the value that stands in for cells nobody writes; a property, so the value carries
    // its own type instead of the caller naming one. there is no getter to pair with it:
    // hdf5 keeps no record of the type a fill value was declared in, so only the dataset
    // can be asked what its fill value is
    cls.def_property(
        // the name
        "fillValue",
        // there is nothing here to read
        nullptr,
        // the setter, which reads the type off the value it is handed
        [](DCPL & self, const py::object & value) -> void {
            // integers travel as 64-bit
            if (py::isinstance<py::int_>(value)) {
                // deposit it
                self.fillValue(value.cast<std::int64_t>());
                // all done
                return;
            }
            // reals as doubles
            if (py::isinstance<py::float_>(value)) {
                // deposit it
                self.fillValue(value.cast<double>());
                // all done
                return;
            }
            // and complex values as pairs of doubles
            if (PyComplex_Check(value.ptr())) {
                // deposit it
                self.fillValue(value.cast<std::complex<double>>());
                // all done
                return;
            }
            // anything else is a caller mistake
            throw py::type_error("unsupported fill value type");
        },
        // the docstring
        "the value that stands in for cells nobody writes; hdf5 converts it to the "
        "dataset's own type when the dataset is created");

    // get the fill value writing time
    cls.def_property(
        // the name
        "fillTime",
        // the getter
        py::overload_cast<>(&DCPL::fillTime, py::const_),
        // the setter
        py::overload_cast<H5D_fill_time_t>(&DCPL::fillTime),
        // the docstring
        "when the fill value is written to storage");
    // set the fill value writing time


    // get the data layout strategy
    cls.def_property(
        // the name
        "layout",
        // the getter
        py::overload_cast<>(&DCPL::layout, py::const_),
        // the setter
        py::overload_cast<H5D_layout_t>(&DCPL::layout),
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
        "addDeflate",
        // the implementation
        &DCPL::addDeflate,
        // the signature
        "level"_a,
        // the docstring
        "use deflate with the given {level}");
    // szip
    cls.def(
        // the name
        "addSzip",
        // the implementation
        &DCPL::addSzip,
        // the signature
        "options"_a, "pixelsPerBlock"_a,
        // the docstring
        "use szip compression with the given {options} and {pixelsPerBlock}");
    // nbit
    cls.def(
        // the name
        "addNbit",
        // the implementation
        &DCPL::addNbit,
        // the docstring
        "use nbit compression");
    // shuffle
    cls.def(
        // the name
        "addShuffle",
        // the implementation
        &DCPL::addShuffle,
        // the docstring
        "use the shuffle filter to improve compression");
    // fletcher32
    cls.def(
        // the name
        "addFletcher32",
        // the implementation
        &DCPL::addFletcher32,
        // the docstring
        "use the fletcher32 checksum filter for error detection");
    // scaleoffset
    cls.def(
        // the name
        "addScaleoffset",
        // the implementation
        &DCPL::addScaleoffset,
        // the signature
        "scaleType"_a, "scaleFactor"_a,
        // the docstring
        "use the scale-offset filter with the given {scaleType} and {scaleFactor}");


    // all done
    return;
}


// end of file
