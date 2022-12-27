// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file objects
void
pyre::h5::py::datatypes::datatype(py::module & m)
{
    // add bindings for the base hdf5 datatype
    auto dataType = py::class_<DataType>(
        // in scope
        m,
        // class name
        "DataType",
        // docstring
        "the base HDF5 datatype");

    // all done
    return;
}


// end of file
