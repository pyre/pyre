// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// dataspaces
void
pyre::h5::py::dataspace(py::module & m)
{
    // add bindings for hdf5 dataspaces
    auto cls = py::class_<DataSpace>(
        // in scope
        m,
        // class name
        "DataSpace",
        // docstring
        "an HDF5 dataspace");


    // all done
    return;
}


// end of file
