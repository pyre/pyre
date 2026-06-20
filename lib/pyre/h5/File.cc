// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "File.h"
// the property lists i hand back
#include "properties/FCPL.h"
#include "properties/FAPL.h"


// open or create the file at {uri}; the read modes open, the others create
pyre::h5::File::File(
    const string_t & uri, unsigned int flags, const properties::FCPL & fcpl,
    const properties::FAPL & fapl) :
    Group(static_cast<id_type>(
        (flags == H5F_ACC_RDONLY || flags == H5F_ACC_RDWR)
            ? H5Fopen(uri.data(), flags, fapl.id())
            : H5Fcreate(uri.data(), flags, fcpl.id(), fapl.id())))
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
    return properties::FCPL(static_cast<id_type>(H5Fget_create_plist(id())));
}


// my access property list, as a fresh owned wrapper
auto
pyre::h5::File::fapl() const -> properties::FAPL
{
    // {H5Fget_access_plist} hands back a fresh handle the wrapper adopts
    return properties::FAPL(static_cast<id_type>(H5Fget_access_plist(id())));
}


// end of file
