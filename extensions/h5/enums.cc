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
    // identifier types
    py::enum_<H5I_type_t>(m, "IdentifierType", "the types of h5 identifiers")
        // add the values
        .value("uninitialized", H5I_UNINIT)
        .value("bad", H5I_BADID)
        .value("file", H5I_FILE)
        .value("group", H5I_GROUP)
        .value("datatype", H5I_DATATYPE)
        .value("dataspace", H5I_DATASPACE)
        .value("dataset", H5I_DATASET)
#if H5_VERSION_GE(1, 12, 0)
        .value("map", H5I_MAP)
#endif
        .value("attr", H5I_ATTR)
        .value("virtual_file_layer", H5I_VFL)
#if H5_VERSION_GE(1, 12, 0)
        .value("virtual_object_layer", H5I_VOL)
#endif
        .value("property_class", H5I_GENPROP_CLS)
        .value("property_list", H5I_GENPROP_LST)
        .value("error_class", H5I_ERROR_CLASS)
        .value("error_message", H5I_ERROR_MSG)
        .value("error_stack", H5I_ERROR_STACK)
#if H5_VERSION_GE(1, 12, 0)
        .value("dataspace_selection_iterator", H5I_SPACE_SEL_ITER)
#endif
#if H5_VERSION_GE(1, 13, 0)
        .value("event_set", H5I_EVENTSET)
#endif
        .value("types", H5I_NTYPES);

    // object types
    py::enum_<H5O_type_t>(m, "ObjectType", "the types of h5 objects")
        // add the values
        .value("unknown", H5O_TYPE_UNKNOWN)
        .value("group", H5O_TYPE_GROUP)
        .value("dataset", H5O_TYPE_DATASET)
        .value("datatype", H5O_TYPE_NAMED_DATATYPE)
#if H5_VERSION_GE(1, 12, 0)
        .value("map", H5O_TYPE_MAP)
#endif
        .value("types", H5O_TYPE_NTYPES);

    // dataset types
    py::enum_<H5T_class_t>(m, "DataSetType", "the types of h5 datasets")
        // add the values
        .value("error", H5T_NO_CLASS)
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

    // dataspace types
    py::enum_<H5S_class_t>(m, "DataSpaceType", "the types of h5 dataspaces")
        // add the values
        .value("error", H5S_NO_CLASS)
        .value("scalar", H5S_SCALAR)
        .value("simple", H5S_SIMPLE)
        .value("null", H5S_NULL);

    // selection operators
    py::enum_<H5S_seloper_t>(m, "SelectionOperator", "the dataspace selection operators")
        .value("noop", H5S_SELECT_NOOP)
        .value("set", H5S_SELECT_SET)
        .value("or_", H5S_SELECT_OR)
        .value("and_", H5S_SELECT_AND)
        .value("xor", H5S_SELECT_XOR)
        .value("a_not_b", H5S_SELECT_NOTB)
        .value("b_not_a", H5S_SELECT_NOTA)
        .value("append", H5S_SELECT_APPEND)
        .value("prepend", H5S_SELECT_PREPEND)
        .value("invalid", H5S_SELECT_INVALID);

    // byte packing order
    py::enum_<H5T_order_t>(m, "ByteOrder", "the byte packing strategies")
        // add the values
        .value("error", H5T_ORDER_ERROR)
        .value("little", H5T_ORDER_LE)
        .value("big", H5T_ORDER_BE)
        .value("vax", H5T_ORDER_VAX)
        .value("mixed", H5T_ORDER_MIXED)
        .value("none", H5T_ORDER_NONE);

    // integer sign schemes
    py::enum_<H5T_sign_t>(m, "Sign", "the sign schemes")
        .value("error", H5T_SGN_ERROR)
        .value("none", H5T_SGN_NONE)    // unsigned types
        .value("complement", H5T_SGN_2) // two's complement
        .value("none", H5T_NSGN);

    // datatype bit padding types
    py::enum_<H5T_pad_t>(m, "PaddingType", "the bit padding strategies")
        // add the values
        .value("error", H5T_PAD_ERROR)
        .value("zero", H5T_PAD_ZERO)
        .value("one", H5T_PAD_ONE)
        .value("background", H5T_PAD_BACKGROUND);

    // floating point mantissa normalization strategies
    py::enum_<H5T_norm_t>(m, "NormalizationType", "the mantissa normalization strategies")
        // add the values
        .value("error", H5T_NORM_ERROR)
        .value("implied", H5T_NORM_IMPLIED)
        .value("set", H5T_NORM_MSBSET)
        .value("none", H5T_NORM_NONE);

    // all done
    return;
}


// end of file
