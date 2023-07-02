// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file access property lists
void
pyre::h5::py::fapl(py::module & m)
{
    // add bindings for hdf5 file access property lists
    auto cls = py::class_<FAPL, PropList>(
        // in scope
        m,
        // class name
        "FAPL",
        // docstring
        "a file access property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) {
            // easy enough
            return &FAPL::DEFAULT;
        },
        // docstring
        "the default file access property list");

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
        &FAPL::getMetaBlockSize,
        // the docstring
        "retrieve the metadata block size");

    // get the metadata block size
    cls.def(
        // the name
        "setMetaBlockSize",
        // the implementation
        &FAPL::setMetaBlockSize,
        // the signature
        "size"_a,
        // the docstring
        "set the metadata cache parameters");

    // get the page buffer characteristics
    cls.def(
        // the name
        "getPageBufferSize",
        // the implementation
        [](const FAPL & self) {
            // make some room
            size_t buffer = 4 * 1024;
            unsigned int meta = 0;
            unsigned int raw = 0;
            // get the info
            H5Pget_page_buffer_size(self.getId(), &buffer, &meta, &raw);
            // pack and ship
            return py::make_tuple(buffer, meta, raw);
        },
        // the docstring
        "retrieve the page buffer characteristics");

    // set the page buffer characteristics
    cls.def(
        // the name
        "setPageBufferSize",
        // the implementation
        [](const FAPL & self, size_t buffer, unsigned int meta, unsigned int raw) {
            // set the values and return
            return H5Pset_page_buffer_size(self.getId(), buffer, meta, raw);
        },
        // the signature
        "page"_a, "meta"_a = 0, "raw"_a = 0,
        // the docstring
        "retrieve the page buffer characteristics");


#if defined(H5_HAVE_ROS3_VFD)
    // populate the property list with ros3 parameters
    cls.def(
        // the name
        "ros3",
        // the implementation
        [](FAPL & self, bool authenticate, string_t region, string_t id, string_t key,
           string_t token) -> FAPL & {
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
            auto status = H5Pset_fapl_ros3(self.getId(), &p);
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
            return self;
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
