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
    // dataset space allocation timing
    py::enum_<H5D_alloc_time_t>(m, "AllocTime", "the timing for allocating dataset space")
        // add the values
        .value("error", H5D_ALLOC_TIME_ERROR)
        .value("default", H5D_ALLOC_TIME_DEFAULT)
        .value("early", H5D_ALLOC_TIME_EARLY)
        .value("late", H5D_ALLOC_TIME_LATE)
        .value("incr", H5D_ALLOC_TIME_INCR);

    // dataset fill timing
    py::enum_<H5D_fill_time_t>(m, "FillTime", "the timing for writing the dataset fill value")
        // add the values
        .value("error", H5D_FILL_TIME_ERROR)
        .value("alloc", H5D_FILL_TIME_ALLOC)
        .value("never", H5D_FILL_TIME_NEVER)
        .value("if_set", H5D_FILL_TIME_IFSET);

    // dataset fill value
    py::enum_<H5D_fill_value_t>(m, "FillValue", "fill value strategies")
        // add the values
        .value("error", H5D_FILL_VALUE_ERROR)
        .value("undefined", H5D_FILL_VALUE_UNDEFINED)
        .value("default", H5D_FILL_VALUE_DEFAULT)
        .value("user_defined", H5D_FILL_VALUE_USER_DEFINED);

    // dataset layout strategy
    py::enum_<H5D_layout_t>(m, "Layout", "dataset layout strategies")
        .value("error", H5D_LAYOUT_ERROR)
        .value("compact", H5D_COMPACT)
        .value("contiguous", H5D_CONTIGUOUS)
        .value("chunked", H5D_CHUNKED)
        .value("virtual", H5D_VIRTUAL)
        .value("layouts", H5D_NLAYOUTS);

    // file space handling strategies
    py::enum_<H5F_fspace_strategy_t>(m, "FilespaceStrategy", "the file space strategies")
        .value("fsm_aggr", H5F_FSPACE_STRATEGY_FSM_AGGR)
        .value("page", H5F_FSPACE_STRATEGY_PAGE)
        .value("aggr", H5F_FSPACE_STRATEGY_AGGR)
        .value("none", H5F_FSPACE_STRATEGY_NONE)
        .value("types", H5F_FSPACE_STRATEGY_NTYPES);

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

    // string character sets
    py::enum_<H5T_cset_t>(m, "CharacterSet", "the string character sets")
        .value("error", H5T_CSET_ERROR)
        .value("ascii", H5T_CSET_ASCII)
        .value("utf8", H5T_CSET_UTF8)
        .value("reserved_2", H5T_CSET_RESERVED_2)
        .value("reserved_3", H5T_CSET_RESERVED_3)
        .value("reserved_4", H5T_CSET_RESERVED_4)
        .value("reserved_5", H5T_CSET_RESERVED_5)
        .value("reserved_6", H5T_CSET_RESERVED_6)
        .value("reserved_7", H5T_CSET_RESERVED_7)
        .value("reserved_8", H5T_CSET_RESERVED_8)
        .value("reserved_9", H5T_CSET_RESERVED_9)
        .value("reserved_10", H5T_CSET_RESERVED_10)
        .value("reserved_11", H5T_CSET_RESERVED_11)
        .value("reserved_12", H5T_CSET_RESERVED_12)
        .value("reserved_13", H5T_CSET_RESERVED_13)
        .value("reserved_14", H5T_CSET_RESERVED_14)
        .value("reserved_15", H5T_CSET_RESERVED_15);

    // floating point mantissa normalization strategies
    py::enum_<H5T_norm_t>(m, "NormalizationType", "the mantissa normalization strategies")
        // add the values
        .value("error", H5T_NORM_ERROR)
        .value("implied", H5T_NORM_IMPLIED)
        .value("set", H5T_NORM_MSBSET)
        .value("none", H5T_NORM_NONE);

    // byte packing order
    py::enum_<H5T_order_t>(m, "ByteOrder", "the byte packing strategies")
        // add the values
        .value("error", H5T_ORDER_ERROR)
        .value("littleEndian", H5T_ORDER_LE)
        .value("bigEndian", H5T_ORDER_BE)
        .value("vax", H5T_ORDER_VAX)
        .value("mixed", H5T_ORDER_MIXED)
        .value("none", H5T_ORDER_NONE);

    // datatype bit padding types
    py::enum_<H5T_pad_t>(m, "PaddingType", "the bit padding strategies")
        // add the values
        .value("error", H5T_PAD_ERROR)
        .value("zero", H5T_PAD_ZERO)
        .value("one", H5T_PAD_ONE)
        .value("background", H5T_PAD_BACKGROUND);

    // integer sign schemes
    py::enum_<H5T_sign_t>(m, "Sign", "the sign schemes")
        .value("error", H5T_SGN_ERROR)
        .value("unsigned", H5T_SGN_NONE) // unsigned types
        .value("complement", H5T_SGN_2)  // two's complement
        .value("null", H5T_NSGN);

    // string padding schemes
    py::enum_<H5T_str_t>(m, "StringPadding", "the string padding schemes")
        .value("error", H5T_STR_ERROR)
        .value("null_terminated", H5T_STR_NULLTERM)
        .value("null_padded", H5T_STR_NULLPAD)
        .value("space_padded", H5T_STR_SPACEPAD)
        .value("reserved_3", H5T_STR_RESERVED_3)
        .value("reserved_4", H5T_STR_RESERVED_4)
        .value("reserved_5", H5T_STR_RESERVED_5)
        .value("reserved_6", H5T_STR_RESERVED_6)
        .value("reserved_7", H5T_STR_RESERVED_7)
        .value("reserved_8", H5T_STR_RESERVED_8)
        .value("reserved_9", H5T_STR_RESERVED_9)
        .value("reserved_10", H5T_STR_RESERVED_10)
        .value("reserved_11", H5T_STR_RESERVED_11)
        .value("reserved_12", H5T_STR_RESERVED_12)
        .value("reserved_13", H5T_STR_RESERVED_13)
        .value("reserved_14", H5T_STR_RESERVED_14)
        .value("reserved_15", H5T_STR_RESERVED_15);

    // all done
    return;
}


// end of file
