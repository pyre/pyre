// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// the package global declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
// namespace setup
#include "forward.h"


// register the class, so that every signature can name it
void
pyre::h5::py::types::atomClass(py::module & m)
{
    // register the class
    py::class_<AtomType, DataType>(
        // in scope
        m,
        // class name
        "atom",
        // docstring
        "an HDF5 atom datatype");

    // all done
    return;
}


// bind the atomic datatypes
void
pyre::h5::py::types::atom()
{
    // the class, registered by {atomClass}
    auto cls = py::class_<AtomType, DataType>(py::type::of<AtomType>());

    // properties
    cls.def_property(
        // the name
        "order",
        // the getter
        &AtomType::order,
        // the setter
        pyre::py::setter(cls, &AtomType::setOrder),
        // the docstring
        "get/set the byte order");

    cls.def_property(
        // the name
        "offset",
        // the getter
        &AtomType::offset,
        // the setter
        pyre::py::setter(cls, &AtomType::setOffset),
        // the docstring
        "get/set the bit offset of the first significant bit");

    cls.def_property(
        // the name
        "pad",
        // the getter
        &AtomType::pad,
        // the setter
        pyre::py::setter(
            cls,
            [](AtomType & self, std::pair<H5T_pad_t, H5T_pad_t> pad) {
                // unpack
                auto [lsb, msb] = pad;
                // and set
                self.setPad(lsb, msb);
                // all done
                return;
            }),
        // the docstring
        "get/set the padding strategy for (lsb, msb)");

    cls.def_property(
        // the name
        "precision",
        // the getter
        &AtomType::precision,
        // the setter
        pyre::py::setter(cls, &AtomType::setPrecision),
        // the docstring
        "get/set the precision");

    cls.def_property(
        // the name
        "bytes",
        // the getter
        &AtomType::bytes,
        // the setter
        pyre::py::setter(cls, &AtomType::setBytes),
        // the docstring
        "get/set the overall size");

    // all done
    return;
}


// end of file
