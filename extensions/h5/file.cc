// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file objects
void
h5::py::file(py::module & m)
{
    // add bindings for hdf5 file objects
    auto cls = py::class_<File>(
        // in scope
        m,
        // class name
        "File",
        // docstring
        "an HDF5 file");

    // constructor
    cls.def(
        // the implementation
        py::init([](std::string name) {
            // make a read-only entity and return it
            return new File(name, H5F_ACC_RDONLY);
        }),
        // the signature
        "path"_a,
        // the docstring
        "open an HDF5 file given its {path}");

    // close a file
    cls.def(
        // the name
        "close",
        // the implementation
        &File::close,
        // the docstring
        "close the file");

    // all done
    return;
}


// end of file
