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
pyre::h5::py::fapl(py::module & m)
{
    // add bindings for hdf5 file objects
    auto cls = py::class_<FileAccessPropertyList>(
        // in scope
        m,
        // class name
        "FAPL",
        // docstring
        "a file access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "create a file access property list");

    // get the metadata block size
    cls.def(
        // the name
        "getMetaBlockSize",
        // the implementation
        &FileAccessPropertyList::getMetaBlockSize,
        // the docstring
        "retrieve the metadata block size");

    // set the page buffer settings
    cls.def(
        // the name
        "setMetaBlockSize",
        // the implementation
        &FileAccessPropertyList::setMetaBlockSize,
        // the signature
        "size"_a,
        // the docstring
        "set the metadata cache parameters");

    // close the list
    cls.def(
        // the name
        "close",
        // the implementation
        &FileAccessPropertyList::close,
        // the docstring
        "discard the property list");

#if defined(H5_HAVE_ROS3_VFD)
    // populate the property list with ros3 parameters
    cls.def(
        // the name
        "ros3",
        // the implementation
        [](FileAccessPropertyList & plist, bool authenticate, string_t region, string_t id,
           string_t key, string_t token) -> FileAccessPropertyList & {
            // make room for the driver parameters
            H5FD_ros3_fapl_t p;
            // populate
            p.version = H5FD_CURR_ROS3_FAPL_T_VERSION;
            p.authenticate = authenticate ? 1 : 0;
            std::strcpy(p.aws_region, region.data());
            std::strcpy(p.secret_id, id.data());
            std::strcpy(p.secret_key, key.data());
#if H5FD_CURR_ROS3_FAPL_T_VERSION > 1
            // the correct versions of libhdf5 have room for a session token
            std::strcpy(p.session_token, token.data());
#endif
            // send to the {ros3} driver; this process includes runtime validation, so there is
            // no need for extra checks that the struct we populated is understood by whatever
            // runtime we have dynamically linked against
            auto status = H5Pset_fapl_ros3(plist.getId(), &p);
            // if the transfer failed
            if (status < 0) {
                // make a channel
                auto channel = pyre::journal::error_t("pyre.h5.fapl");
                // complain
                channel
                    // complain
                    << "failed to populate a file access property list with ros3 parameters"
                    << pyre::journal::newline
                    // and flush
                    << pyre::journal::endl(__HERE__);
            }
            // all done
            return plist;
        },
        // the signature
        "authenticate"_a = true, "region"_a = "", "id"_a = "", "key"_a = "", "token"_a = "",
        // the docstring
        "populate the property list with ros3 parameters");
#endif

    // all done
    return;
}


// end of file
