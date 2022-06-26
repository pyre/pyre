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
pyre::h5::py::file(py::module & m)
{
    // add bindings for hdf5 file objects
    auto cls = py::class_<File, Group>(
        // in scope
        m,
        // class name
        "File",
        // docstring
        "an HDF5 file");

    // constructor
    cls.def(
        // the implementation
        py::init([](std::string path, std::string mode) {
            // valid modes, per {h5py}
            //    r: read-only, file must exist
            //   r+: read/write, file must exist
            //    w: create file, truncate if it exists
            //   w-: create file, fail if it exists
            //    x: alias for avove
            //    a: create if it doesn't exist, read/write regardless

            // for now, make a read-only entity and return it
            return new File(path, H5F_ACC_RDONLY);
        }),
        // the signature
        "path"_a, "mode"_a = "r",
        // the docstring
        "open an HDF5 file given its {path}");

    // close the file
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
