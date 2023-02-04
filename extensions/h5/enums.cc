// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the various H5 enums
void
pyre::h5::py::enums(py::module & m)
{
    // object types
    py::enum_<H5O_type_t>(m, "ObjectType", "the types of h5 objects")
        // add the values
        .value("unknown", H5O_TYPE_UNKNOWN)
        .value("group", H5O_TYPE_GROUP)
        .value("dataset", H5O_TYPE_DATASET)
        .value("datatype", H5O_TYPE_NAMED_DATATYPE)
        .value("map", H5O_TYPE_MAP)
        .value("types", H5O_TYPE_NTYPES);

    // dataset types
    py::enum_<H5T_class_t>(m, "DatasetType", "the types of h5 datasets")
        // add the values
        .value("none", H5T_NO_CLASS)
        .value("int", H5T_INTEGER)
        .value("float", H5T_FLOAT)
        .value("timestamp", H5T_TIME)
        .value("str", H5T_STRING)
        .value("bits", H5T_BITFIELD)
        .value("opaque", H5T_OPAQUE)
        .value("compound", H5T_COMPOUND)
        .value("ref", H5T_REFERENCE)
        .value("enum", H5T_ENUM)
        .value("vlen", H5T_VLEN)
        .value("array", H5T_ARRAY)
        .value("classes", H5T_NCLASSES);

    // byte packing order
    py::enum_<H5T_order_t>(m, "ByteOrder", "the byte packing strategies")
        // add the values
        .value("error", H5T_ORDER_ERROR)
        .value("little", H5T_ORDER_LE)
        .value("big", H5T_ORDER_BE)
        .value("vax", H5T_ORDER_VAX)
        .value("mixed", H5T_ORDER_MIXED)
        .value("none", H5T_ORDER_NONE);


    // all done
    return;
}


// end of file
