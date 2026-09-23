// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "FAPL.h"
// the reporting of library refusals
#include "../diagnostics.h"
// for populating the ros3 driver parameter struct
#include <cstring>


// make a fresh file access property list
pyre::h5::properties::FAPL::FAPL() : List(H5Pcreate(H5P_FILE_ACCESS))
{
    // if the library refused to make it
    if (!valid()) {
        // complain
        complain("pyre.h5.fapl", "creating a file access property list");
    }
}


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
pyre::h5::properties::FAPL::metadataBlockSize() const -> hsize_t
{
    // make room for the answer
    hsize_t size = 0;
    // ask the library
    if (H5Pget_meta_block_size(id(), &size) < 0) {
        // complain if it refused
        complain("pyre.h5.fapl", "retrieving the metadata block size");
        // and report nothing
        return 0;
    }
    // otherwise, report
    return size;
}


// set the metadata block size
auto
pyre::h5::properties::FAPL::metadataBlockSize(hsize_t size) -> void
{
    // hand it to the library
    if (H5Pset_meta_block_size(id(), size) < 0) {
        // and complain if it refused
        complain("pyre.h5.fapl", "setting the metadata block size");
    }
    // all done
    return;
}


// the page buffer characteristics: (bytes, metadata percent, raw-data percent)
auto
pyre::h5::properties::FAPL::pageBufferSize() const -> PageBuffer
{
    // make room for the answer
    std::size_t buffer = 0;
    unsigned int meta = 0;
    unsigned int raw = 0;
    // ask the library
    if (H5Pget_page_buffer_size(id(), &buffer, &meta, &raw) < 0) {
        // complain if it refused
        complain("pyre.h5.fapl", "retrieving the page buffer settings");
        // and report an empty buffer
        return PageBuffer(0, 0, 0);
    }
    // otherwise, pack and ship
    return PageBuffer(buffer, meta, raw);
}


// set the page buffer characteristics
auto
pyre::h5::properties::FAPL::pageBufferSize(const PageBuffer & buffer) -> void
{
    // hand them to the library
    if (H5Pset_page_buffer_size(id(), buffer.bytes, buffer.metadata, buffer.raw) < 0) {
        // and complain if it refused
        complain("pyre.h5.fapl", "setting the page buffer");
    }
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
        // complain if the library refused
        complain("pyre.h5.fapl", "populating a file access property list with ros3 parameters");
        // and leave the list as it was
        return *this;
    }
    // attach the security token for temporary credentials
    if (H5Pset_fapl_ros3_token(this->id(), token.data()) < 0) {
        // and complain if the library refused it
        complain("pyre.h5.fapl", "attaching the ros3 session token");
    }
    // hand off a reference to me
    return *this;
}
#endif


// the alignment of objects in the file
auto
pyre::h5::properties::FAPL::alignment() const -> Alignment
{
    // make room for the answer
    hsize_t threshold = 0;
    hsize_t alignment = 0;
    // ask the library
    if (H5Pget_alignment(id(), &threshold, &alignment) < 0) {
        // complain if it refused
        complain("pyre.h5.fapl", "retrieving the object alignment");
        // and report no alignment
        return Alignment(0, 0);
    }
    // otherwise, pack and ship
    return Alignment(threshold, alignment);
}


// set the alignment of objects in the file
auto
pyre::h5::properties::FAPL::alignment(const Alignment & alignment) -> void
{
    // hand them to the library
    if (H5Pset_alignment(id(), alignment.threshold, alignment.boundary) < 0) {
        // and complain if it refused
        complain("pyre.h5.fapl", "setting the object alignment");
    }
    // all done
    return;
}


// the size of the sieve buffer
auto
pyre::h5::properties::FAPL::sieveBufferSize() const -> std::size_t
{
    // make room for the answer
    std::size_t size = 0;
    // ask the library
    if (H5Pget_sieve_buf_size(id(), &size) < 0) {
        // complain if it refused
        complain("pyre.h5.fapl", "retrieving the sieve buffer size");
        // and report nothing
        return 0;
    }
    // otherwise, report
    return size;
}


// set the size of the sieve buffer
auto
pyre::h5::properties::FAPL::sieveBufferSize(std::size_t size) -> void
{
    // hand it to the library
    if (H5Pset_sieve_buf_size(id(), size) < 0) {
        // and complain if it refused
        complain("pyre.h5.fapl", "setting the sieve buffer size");
    }
    // all done
    return;
}


// what happens to a file whose handle is closed while objects in it are still open
auto
pyre::h5::properties::FAPL::closeDegree() const -> H5F_close_degree_t
{
    // make room for the answer
    H5F_close_degree_t degree = H5F_CLOSE_DEFAULT;
    // ask the library
    if (H5Pget_fclose_degree(id(), &degree) < 0) {
        // complain if it refused
        complain("pyre.h5.fapl", "retrieving the file close degree");
        // and report the library default
        return H5F_CLOSE_DEFAULT;
    }
    // otherwise, report
    return degree;
}


// set the file close degree
auto
pyre::h5::properties::FAPL::closeDegree(H5F_close_degree_t degree) -> void
{
    // hand it to the library
    if (H5Pset_fclose_degree(id(), degree) < 0) {
        // and complain if it refused
        complain("pyre.h5.fapl", "setting the file close degree");
    }
    // all done
    return;
}


// the default caches
auto
pyre::h5::properties::FAPL::cache() const -> Cache
{
    // make room for the answer
    int elements = 0;
    std::size_t slots = 0;
    std::size_t bytes = 0;
    double w0 = 0;
    // ask the library
    if (H5Pget_cache(id(), &elements, &slots, &bytes, &w0) < 0) {
        // complain if it refused
        complain("pyre.h5.fapl", "retrieving the cache settings");
        // and report an empty cache
        return Cache(0, 0, 0, 0);
    }
    // otherwise, pack and ship
    return Cache(elements, slots, bytes, w0);
}


// set the default caches
auto
pyre::h5::properties::FAPL::cache(const Cache & cache) -> void
{
    // hand them to the library
    if (H5Pset_cache(id(), cache.metadataElements, cache.slots, cache.bytes, cache.preemption)
        < 0) {
        // and complain if it refused
        complain("pyre.h5.fapl", "setting the caches");
    }
    // all done
    return;
}


// the bounds on the file format versions hdf5 may use
auto
pyre::h5::properties::FAPL::libverBounds() const -> VersionBounds
{
    // make room for the answer
    H5F_libver_t low = H5F_LIBVER_EARLIEST;
    H5F_libver_t high = H5F_LIBVER_LATEST;
    // ask the library
    if (H5Pget_libver_bounds(id(), &low, &high) < 0) {
        // complain if it refused
        complain("pyre.h5.fapl", "retrieving the file format version bounds");
        // and report the widest bounds
        return VersionBounds(H5F_LIBVER_EARLIEST, H5F_LIBVER_LATEST);
    }
    // otherwise, pack and ship
    return VersionBounds(low, high);
}


// set the bounds on the file format versions
auto
pyre::h5::properties::FAPL::libverBounds(const VersionBounds & bounds) -> void
{
    // hand them to the library
    if (H5Pset_libver_bounds(id(), bounds.low, bounds.high) < 0) {
        // and complain if it refused
        complain("pyre.h5.fapl", "setting the file format version bounds");
    }
    // all done
    return;
}


// end of file
