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

    // constructor for accessing a local file
    cls.def(
        // the implementation
        py::init([](std::string uri, std::string mode) {
            // decode mode
            if (mode == "r") {
                // read-only, file must exist
                return File(uri, H5F_ACC_RDONLY);
            }
            if (mode == "r+") {
                // read/write, file must exist
                return File(uri, H5F_ACC_RDWR);
            }
            if (mode == "w") {
                // create file, truncate if it exists
                return File(uri, H5F_ACC_TRUNC);
            }
            if (mode == "w-" || mode == "x") {
                // create file, fail if it exists
                return File(uri, H5F_ACC_EXCL);
            }

            // h5py has one more valid {mode}
            // a: create if it doesn't exist, read/write regardless
            // supporting this requires attempting to open the file in RDWR mode
            // and trying again in EXCL if it fails
            // i need to learn a bit more about error trapping before attempting this

            // if we get this far, we have a problem
            auto channel = pyre::journal::error_t("pyre.h5.file");
            // so complain
            channel
                // say why
                << "invalid mode '" << mode << "'"
                << pyre::journal::newline
                // show me the filename
                << "while opening '" << uri << "'"
                << pyre::journal::newline
                // show me what's supported
                << "currently supported modes: r, r+, w, w-"
                // and flush
                << pyre::journal::endl(__HERE__);

            // just in case this error is not fatal, make a stub
            return File();
        }),
        // the signature
        "uri"_a, "mode"_a = "r",
        // the docstring
        "open an HDF5 file given its {uri}");

    // constructor for accessing a file with a custom access property list
    cls.def(
        // the implementation
        py::init([](std::string uri, const FileAccessPropertyList & p, std::string mode) {
            // decode mode
            if (mode == "r") {
                // read-only, file must exist
                return File(uri, H5F_ACC_RDONLY, FileCreatePropertyList::DEFAULT, p);
            }
            if (mode == "r+") {
                // read/write, file must exist
                return File(uri, H5F_ACC_RDWR, FileCreatePropertyList::DEFAULT, p);
            }
            if (mode == "w") {
                // create file, truncate if it exists
                return File(uri, H5F_ACC_TRUNC, FileCreatePropertyList::DEFAULT, p);
            }
            if (mode == "w-" || mode == "x") {
                // create file, fail if it exists
                return File(uri, H5F_ACC_EXCL, FileCreatePropertyList::DEFAULT, p);
            }

            // h5py has one more valid {mode}
            // a: create if it doesn't exist, read/write regardless
            // supporting this requires attempting to open the file in RDWR mode
            // and trying again in EXCL if it fails
            // i need to learn a bit more about error trapping before attempting this

            // if we get this far, we have a problem
            auto channel = pyre::journal::error_t("pyre.h5.file");
            // so complain
            channel
                // say why
                << "invalid mode '" << mode << "'"
                << pyre::journal::newline
                // show me the filename
                << "while opening '" << uri << "'"
                << pyre::journal::newline
                // show me what's supported
                << "currently supported modes: r, r+, w, w-"
                // and flush
                << pyre::journal::endl(__HERE__);

            // just in case this error is not fatal, make a stub
            return File();
        }),
        // the signature
        "uri"_a, "fapl"_a, "mode"_a = "r",
        // the docstring
        "open an HDF5 file given its {uri} and a custom access property list");

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
