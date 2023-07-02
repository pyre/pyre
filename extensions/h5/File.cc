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

    // constructor
    cls.def(
        // the implementation
        py::init([](string_t uri, string_t mode, const FCPL & fcpl, const FAPL & fapl) {
            // decode mode
            if (mode == "r") {
                // read-only, file must exist
                return File(uri, H5F_ACC_RDONLY, fcpl, fapl);
            }
            if (mode == "r+") {
                // read/write, file must exist
                return File(uri, H5F_ACC_RDWR, fcpl, fapl);
            }
            if (mode == "w") {
                // create file, truncate if it exists
                return File(uri, H5F_ACC_TRUNC, fcpl, fapl);
            }
            if (mode == "w-" || mode == "x") {
                // create file, fail if it exists
                return File(uri, H5F_ACC_EXCL, fcpl, fapl);
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
        "uri"_a, "mode"_a = "r", "fcpl"_a = FCPL::DEFAULT, "fapl"_a = FAPL::DEFAULT,
        // the docstring
        "open an HDF5 file given its {uri} and a custom access property list");

    // the identifier category
    cls.def_property_readonly_static(
        // the name
        "identifierType",
        // the implementation
        [](const py::object &) -> H5I_type_t {
            // i am a file
            return H5I_FILE;
        },
        // the docstring
        "get my h5 object category");

    // creation property list
    cls.def_property_readonly(
        // the name
        "fcpl",
        // the implementation
        &File::getCreatePlist,
        // the docstring
        "get my creation property list");

    // access property list
    cls.def_property_readonly(
        // the name
        "fapl",
        // the implementation
        &File::getAccessPlist,
        // the docstring
        "get my access property list");

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
