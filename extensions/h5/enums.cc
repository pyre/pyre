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
    py::enum_<H5O_type_t>(m, "ObjectTypes", "the types of h5 objects")
        // add the values
        .value("unknown", H5O_TYPE_UNKNOWN)
        .value("group", H5O_TYPE_GROUP)
        .value("dataset", H5O_TYPE_DATASET)
        .value("datatype", H5O_TYPE_NAMED_DATATYPE)
        .value("map", H5O_TYPE_MAP)
        .value("types", H5O_TYPE_NTYPES);

    // all done
    return;
}


// end of file
