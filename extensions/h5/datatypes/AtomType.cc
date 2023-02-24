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
pyre::h5::py::datatypes::atom(py::module & m)
{
    // add the class
    auto cls = py::class_<AtomType, DataType>(
        // in scope
        m,
        // class name
        "AtomType",
        // docstring
        "an HDF5 atom datatype");

    // properties
    cls.def_property(
        // the name
        "order",
        // the getter
        [](const AtomType & self) {
            // get the byte order and return it
            return self.getOrder();
        },
        // the setter
        &AtomType::setOrder,
        // the docstring
        "get/set the byte order");

    cls.def_property(
        // the name
        "offset",
        // the getter
        &AtomType::getOffset,
        // the setter
        &AtomType::setOffset,
        // the docstring
        "get/set the bit offset of the first significant bit");

    cls.def_property(
        // the name
        "pad",
        // the getter
        [](AtomType & self) {
            // make some room
            H5T_pad_t lsb, msb;
            // read the padding types
            self.getPad(lsb, msb);
            // and return them
            return std::make_pair(lsb, msb);
        },
        // the setter
        [](AtomType & self, std::pair<H5T_pad_t, H5T_pad_t> pad) {
            // unpack
            auto [lsb, msb] = pad;
            // and set
            self.setPad(lsb, msb);
            // all done
            return;
        },
        // the docstring
        "get/set the padding strategy for (lsb, msb)");

    cls.def_property(
        // the name
        "precision",
        // the getter
        &AtomType::getPrecision,
        // the setter
        &AtomType::setPrecision,
        // the docstring
        "get/set the precision");

    cls.def_property(
        // the name
        "bytes",
        // the getter
        &AtomType::getSize,
        // the setter
        &AtomType::setSize,
        // the docstring
        "get/set the overall size");

    // all done
    return;
}


// end of file
