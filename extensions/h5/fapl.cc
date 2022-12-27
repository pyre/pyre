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
        [](FileAccessPropertyList & plist, std::string region, std::string id,
           std::string key) -> FileAccessPropertyList & {
            // make room for the driver parameters
            H5FD_ros3_fapl_t p;
            // populate
            p.version = H5FD_CURR_ROS3_FAPL_T_VERSION;
            p.authenticate = 0;
            std::strcpy(p.aws_region, region.data());
            std::strcpy(p.secret_id, id.data());
            std::strcpy(p.secret_key, key.data());
            // and transfer
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
        "region"_a = "us-east-1", "id"_a = "", "key"_a = "",
        // the docstring
        "populate the property list with ros3 parameters");
#endif

    // all done
    return;
}


// end of file
