// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


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
            // decode mode; {fcpl} and {fapl} are pyre wrappers the {File} ctor takes natively
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
        "uri"_a, "mode"_a = "r", "fcpl"_a = FCPL::theDefault(), "fapl"_a = FAPL::theDefault(),
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
        [](const File & self) -> FCPL {
            // hand back my creation property list as an owned pyre wrapper
            return self.fcpl();
        },
        // the docstring
        "get my creation property list");

    // access property list
    cls.def_property_readonly(
        // the name
        "fapl",
        // the implementation
        [](const File & self) -> FAPL {
            // hand back my access property list as an owned pyre wrapper
            return self.fapl();
        },
        // the docstring
        "get my access property list");

    // what i have open
    cls.def(
        // the name
        "handles",
        // the implementation
        [](const File & self) -> py::dict {
            // the kinds of handle that keep a file open, by name
            const std::vector<std::pair<const char *, unsigned int>> kinds {
                { "file", H5F_OBJ_FILE },       { "group", H5F_OBJ_GROUP },
                { "dataset", H5F_OBJ_DATASET }, { "datatype", H5F_OBJ_DATATYPE },
                { "attribute", H5F_OBJ_ATTR },
            };
            // make a table
            auto census = py::dict();
            // go through the kinds
            for (const auto & [name, kind] : kinds) {
                // count the open handles of this kind
                const auto count = self.handles(kind);
                // and record the ones that exist
                if (count > 0) {
                    census[name] = count;
                }
            }
            // hand it off
            return census;
        },
        // the docstring
        "count the open handles that refer to me or to my contents, by kind; i stay open for "
        "as long as any of them is alive");

    // my size
    cls.def_property_readonly(
        // the name
        "bytes",
        // the implementation
        [](const File & self) -> py::object {
            // ask
            auto size = self.bytes();
            // a size the library could not tell
            if (!size) {
                // comes back empty
                return py::none();
            }
            // otherwise, hand it off
            return py::cast(*size);
        },
        // the docstring
        "my size in bytes, user block and unused space at the end included, or {None} when "
        "the library cannot tell");

    // what my page buffer has seen
    cls.def_property_readonly(
        // the name
        "pageBuffer",
        // the implementation
        [](const File & self) -> py::object {
            // ask
            auto stats = self.pageBuffer();
            // a file opened without a page buffer has no tally
            if (!stats) {
                // and says so
                return py::none();
            }
            // otherwise, hand it off
            return py::cast(*stats);
        },
        // the docstring
        "what my page buffer has seen since i was opened or since its tally was last reset, "
        "or {None} when i was opened without one");

    // start the tally over
    cls.def(
        // the name
        "resetPageBuffer",
        // the implementation
        &File::resetPageBuffer,
        // the docstring
        "start the tally of my page buffer over; {False} when there is no buffer to reset");

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
