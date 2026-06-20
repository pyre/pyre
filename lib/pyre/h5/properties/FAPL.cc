// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "FAPL.h"
// for populating the ros3 driver parameter struct
#include <cstring>


// make a fresh file access property list
pyre::h5::properties::FAPL::FAPL() : List(H5Pcreate(H5P_FILE_ACCESS)) {}


// adopt an existing raw handle
pyre::h5::properties::FAPL::FAPL(id_type id) : List(id) {}


// the shared default file access property list
auto
pyre::h5::properties::FAPL::theDefault() -> const FAPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const FAPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// the metadata block size
auto
pyre::h5::properties::FAPL::metaBlockSize() const -> hsize_t
{
    // make room for the answer
    hsize_t size = 0;
    // ask the library
    H5Pget_meta_block_size(id(), &size);
    // and report
    return size;
}


// set the metadata block size
auto
pyre::h5::properties::FAPL::setMetaBlockSize(hsize_t size) -> void
{
    // hand it to the library
    H5Pset_meta_block_size(id(), size);
    // all done
    return;
}


// the page buffer characteristics: (bytes, metadata percent, raw-data percent)
auto
pyre::h5::properties::FAPL::pageBufferSize() const
    -> std::tuple<std::size_t, unsigned int, unsigned int>
{
    // make room for the answer
    std::size_t buffer = 0;
    unsigned int meta = 0;
    unsigned int raw = 0;
    // ask the library
    H5Pget_page_buffer_size(id(), &buffer, &meta, &raw);
    // pack and ship
    return { buffer, meta, raw };
}


// set the page buffer characteristics
auto
pyre::h5::properties::FAPL::setPageBufferSize(
    std::size_t buffer, unsigned int meta, unsigned int raw) -> void
{
    // hand them to the library
    H5Pset_page_buffer_size(id(), buffer, meta, raw);
    // all done
    return;
}


#if defined(H5_HAVE_ROS3_VFD)
// configure the read-only S3 virtual file driver
auto
pyre::h5::properties::FAPL::ros3(
    bool authenticate, string_t region, string_t id, string_t key, string_t token) -> FAPL &
{
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
    // send to the {ros3} driver; this includes runtime validation, so no extra checks are needed
    if (H5Pset_fapl_ros3(this->id(), &p) < 0) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.h5.fapl");
        // and complain
        channel
            // what
            << "failed to populate a file access property list with ros3 parameters"
            // where
            << pyre::journal::endl(__HERE__);
    }
#if H5_VERSION_GE(1, 14, 2)
    // attach the security token for temporary credentials
    H5Pset_fapl_ros3_token(this->id(), token.data());
#endif
    // hand off a reference to me
    return *this;
}
#endif


// end of file
