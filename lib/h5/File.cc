// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "File.h"
// the reporting of library refusals
#include "diagnostics.h"
// the property lists i hand back
#include "properties/FCPL.h"
#include "properties/FAPL.h"
// the tally of my page buffer
#include "PageBufferStats.h"


// open or create the file at {uri}; the read modes open, the others create
pyre::h5::File::File(
    const string_t & uri, unsigned int flags, const properties::FCPL & fcpl,
    const properties::FAPL & fapl) :
    Group(
        static_cast<id_type>(
            (flags == H5F_ACC_RDONLY || flags == H5F_ACC_RDWR) ?
                H5Fopen(uri.data(), flags, fapl.id()) :
                H5Fcreate(uri.data(), flags, fcpl.id(), fapl.id())))
{}


// an empty file handle, e.g. for a failed open
pyre::h5::File::File() : Group(static_cast<id_type>(H5I_INVALID_HID)) {}


// adopt an existing raw handle
pyre::h5::File::File(id_type id) : Group(id) {}


// my creation property list, as a fresh owned wrapper
auto
pyre::h5::File::fcpl() const -> properties::FCPL
{
    // {H5Fget_create_plist} hands back a fresh handle the wrapper adopts
    auto hid = H5Fget_create_plist(id());
    // if the library refused
    if (hid < 0) {
        // complain
        complain("pyre.h5.file", "retrieving the creation property list of a file");
    }
    // hand off the list, empty if the library refused
    return properties::FCPL(static_cast<id_type>(hid));
}


// my access property list, as a fresh owned wrapper
auto
pyre::h5::File::fapl() const -> properties::FAPL
{
    // {H5Fget_access_plist} hands back a fresh handle the wrapper adopts
    auto hid = H5Fget_access_plist(id());
    // if the library refused
    if (hid < 0) {
        // complain
        complain("pyre.h5.file", "retrieving the access property list of a file");
    }
    // hand off the list, empty if the library refused
    return properties::FAPL(static_cast<id_type>(hid));
}


// the number of open handles of the given {kinds} that refer to me or to my contents
auto
pyre::h5::File::handles(unsigned int kinds) const -> long
{
    // ask the library; it answers with a negative number when it cannot tell
    return static_cast<long>(H5Fget_obj_count(id(), kinds));
}


// my size, in bytes
auto
pyre::h5::File::bytes() const -> std::optional<hsize_t>
{
    // make room for the answer
    hsize_t size = 0;
    // ask
    auto status = H5Fget_filesize(id(), &size);
    // if the library refused
    if (status < 0) {
        // complain
        complain("pyre.h5.file", "retrieving the size of a file");
        // and decline to answer
        return {};
    }
    // hand off the size
    return size;
}


// what my page buffer has seen
auto
pyre::h5::File::pageBuffer() const -> std::optional<PageBufferStats>
{
    // a file opened without a page buffer has no tally, and the library treats the question as
    // an error; screen it here, since the answer is simply that there is nothing to report
    if (fapl().pageBufferSize().bytes == 0) {
        // so report the absence
        return {};
    }
    // make room for the tally
    auto accesses = PageBufferStats::counts_type {};
    auto hits = PageBufferStats::counts_type {};
    auto misses = PageBufferStats::counts_type {};
    auto evictions = PageBufferStats::counts_type {};
    auto bypasses = PageBufferStats::counts_type {};
    // ask
    auto status = H5Fget_page_buffering_stats(
        id(), accesses.data(), hits.data(), misses.data(), evictions.data(), bypasses.data());
    // if the library refused
    if (status < 0) {
        // complain
        complain("pyre.h5.file", "retrieving the page buffer statistics of a file");
        // and decline to answer
        return {};
    }
    // hand off the tally
    return PageBufferStats(accesses, hits, misses, evictions, bypasses);
}


// start the tally of my page buffer over
auto
pyre::h5::File::resetPageBuffer() const -> bool
{
    // a file opened without a page buffer has nothing to start over
    if (fapl().pageBufferSize().bytes == 0) {
        // so say so
        return false;
    }
    // ask
    auto status = H5Freset_page_buffering_stats(id());
    // if the library refused
    if (status < 0) {
        // complain
        complain("pyre.h5.file", "resetting the page buffer statistics of a file");
        // and report the failure
        return false;
    }
    // all done
    return true;
}


// end of file
