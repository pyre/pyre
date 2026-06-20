// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


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
pyre::h5::py::types::float_(py::module & m)
{
    // add the class
    auto cls = py::class_<FloatType, AtomType>(
        // in scope
        m,
        // class name
        "float",
        // docstring
        "an HDF5 float datatype");

    // constructors
    // from an existing type
    cls.def(
        // the implementation
        py::init([](hid_t id) {
            // {id} belongs to someone else; take out a reference of my own, then adopt it
            H5Iinc_ref(id);
            return FloatType(id);
        }),
        // the signature
        "id"_a,
        // the docstring
        "make a float type using the id of an existing one");

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
        &FloatType::bias,
        // the setter
        &FloatType::setBias,
        // the docstring
        "get/set the exponent bias");

    cls.def_property(
        // the name
        "normalization",
        // the getter
        &FloatType::normalization,
        // the setter
        &FloatType::setNorm,
        // the docstring
        "get/set the mantissa normalization strategy");

    cls.def_property(
        // the name
        "inpad",
        // the getter
        &FloatType::inpad,
        // the setter
        &FloatType::setInpad,
        // the docstring
        "get/set the internal padding for unused bits");

    cls.def_property(
        // the name
        "fields",
        // the getter
        &FloatType::fields,
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
        "get/set the bit layout (sign, exponent, mantissa)");

    // all done
    return;
}


// end of file
