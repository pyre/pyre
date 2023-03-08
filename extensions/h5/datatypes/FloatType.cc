// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// the package globla declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
// namespace setup
#include "forward.h"


// file objects
void
pyre::h5::py::datatypes::float_(py::module & m)
{
    // add the class
    auto cls = py::class_<FloatType, AtomType>(
        // in scope
        m,
        // class name
        "FloatType",
        // docstring
        "an HDF5 float datatype");

    // constructors
    // from a predefined float type
    cls.def(
        // the implementation
        py::init<const PredType &>(),
        // the signature
        "type"_a,
        // the docstring
        "make a copy of the predefined {type}");

    // properties
    cls.def_property(
        // the name
        "bias",
        // the getter
        &FloatType::getEbias,
        // the setter
        &FloatType::setEbias,
        // the docstring
        "get/set the exponent bias");

    cls.def_property(
        // the name
        "normalization",
        // the getter
        [](const FloatType & self) {
            // bypass the silly C++ interface that generates a textual representation of the enum
            return H5Tget_norm(self.getId());
        },
        // the setter
        &FloatType::setNorm,
        // the docstring
        "get/set the mantissa normalization strategy");

    cls.def_property(
        // the name
        "inpad",
        // the getter
        [](const FloatType & self) {
            // bypass the silly C++ interface that generates a textual representation of the enum
            return H5Tget_inpad(self.getId());
        },
        // the setter
        &FloatType::setInpad,
        // the docstring
        "get/set the internal padding for unused bits");

    cls.def_property(
        // the name
        "fields",
        // the getter
        [](FloatType & self) {
            // make some room
            std::size_t spos, epos, esize, mpos, msize;
            // read the fields
            self.getFields(spos, epos, esize, mpos, msize);
            // and return them
            return std::make_tuple(spos, epos, esize, mpos, msize);
        },
        // the setter
        [](FloatType & self,
           std::tuple<std::size_t, std::size_t, std::size_t, std::size_t, std::size_t> fields) {
            // unpack
            auto [spos, epos, esize, mpos, msize] = fields;
            // and set
            self.setFields(spos, epos, esize, mpos, msize);
            // all done
            return;
        },
        // the docstring
        "get/set the padding strategy for (lsb, msb)");

    // all done
    return;
}


// end of file
