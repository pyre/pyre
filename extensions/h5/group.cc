// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// objects
void
pyre::h5::py::group(py::module & m)
{
    // add bindings for hdf5 groups
    auto cls = py::class_<Group>(
        // in scope
        m,
        // class name
        "Group",
        // docstring
        "an HDF5 group");

    // close the group
    cls.def(
        // the name
        "close",
        // the implementation
        &Group::close,
        // the docstring
        "close this group");

    // open a dataset
    cls.def(
        // the name
        "dataset",
        // the implementation
        [](const Group & self, string_t path) { return self.openDataSet(path); },
        // the signature
        "path"_a,
        // the docstring
        "open a dataset given its path");

    // all done
    return;
}


// end of file
